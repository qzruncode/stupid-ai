#!/usr/bin/env node
const { spawnSync } = require("child_process");
const { existsSync, mkdirSync, readFileSync, writeFileSync, appendFileSync, unlinkSync, readdirSync } = require("fs");
const { join, resolve } = require("path");

const cwd = process.cwd();
const loopDir = join(cwd, "docs", "human-plans", ".loop");
const statePath = join(loopDir, "state.json");
const stopPath = join(loopDir, "STOP");
const runLogPath = join(loopDir, "run-log.md");
const tokenLedgerPath = join(loopDir, "token-ledger.md");

function ensureLoopDir() {
  mkdirSync(join(loopDir, "batches"), { recursive: true });
  ensureFile(runLogPath, "# Human Plan Loop Run Log\n\n");
  ensureFile(tokenLedgerPath, "# Token Ledger\n\n| Time | Tick | Action | Input | Output | Total | Source |\n|---|---:|---|---:|---:|---:|---|\n");
  ensureFile(join(loopDir, "gates.md"), "# Human Plan Loop Gates\n\n");
  ensureFile(join(loopDir, "changelog.md"), "# Human Plan Loop Changelog\n\n");
  ensureFile(join(loopDir, "batch-index.md"), "# Human Plan Loop Batch Index\n\n");
}

function ensureFile(path, content) {
  if (!existsSync(path)) writeFileSync(path, content);
}

function readState() {
  if (!existsSync(statePath)) return {};
  try {
    return JSON.parse(readFileSync(statePath, "utf8"));
  } catch {
    return {};
  }
}

function writeState(state) {
  writeFileSync(statePath, `${JSON.stringify(state, null, 2)}\n`);
}

function nowIso() {
  return new Date().toISOString();
}

function defaultBatchId() {
  const datePart = nowIso().slice(0, 10).replace(/-/g, "");
  const batchDir = join(loopDir, "batches");
  const ids = [];
  if (existsSync(batchDir)) {
    for (const name of readdirSync(batchDir)) {
      const match = name.match(new RegExp(`^${datePart}-(\\d{3})\\.md$`));
      if (match) ids.push(Number.parseInt(match[1], 10));
    }
  }
  const current = readState().batch_id || "";
  const currentMatch = current.match(new RegExp(`^${datePart}-(\\d{3})$`));
  if (currentMatch) ids.push(Number.parseInt(currentMatch[1], 10));
  const next = ids.length ? Math.max(...ids) + 1 : 1;
  return `${datePart}-${String(next).padStart(3, "0")}`;
}

function estimateTokens(text) {
  return Math.ceil(Array.from(text).length / 4);
}

function parseMaxTicks(value) {
  const parsed = Number.parseInt(value || "3", 10);
  if (!Number.isFinite(parsed) || parsed < 1) return 3;
  return parsed;
}

function logRun(message) {
  appendFileSync(runLogPath, `- ${nowIso()} ${message}\n`);
}

function logTokens(tick, action, input, output, source = "estimated") {
  const inputTokens = estimateTokens(input);
  const outputTokens = estimateTokens(output);
  const total = inputTokens + outputTokens;
  appendFileSync(tokenLedgerPath, `| ${nowIso()} | ${tick} | ${action} | ${inputTokens} | ${outputTokens} | ${total} | ${source} |\n`);
  return total;
}

function claudePrompt(tick, maxTicks) {
  return [
    "/human-plan:loop tick",
    "",
    "Runner context:",
    `- cwd: ${cwd}`,
    "- loop_dir: docs/human-plans/.loop",
    `- tick: ${tick}`,
    `- max_ticks: ${maxTicks}`,
    "",
    "执行一个 tick。只推进一个明确动作，维护 state.json、batch-index.md、run-log.md、gates.md、changelog.md 和 token-ledger.md。",
    "如果没有 active batch，先走 batch-code-scan；如果已有 batch，按 batch-index 顺序只处理当前 active Plan；没有 active Plan 时才选择第一个 pending Plan。",
    "遇到 approve/confirm/人类决策时，把当前 Plan 写入 gates.md 并标为 gated，整个 batch 暂停等待这个 Plan 的人类输入；不得跳过 gated Plan 去处理后续 pending Plan。",
    "只有所有 Plan 都是 complete 且代码状态已固化时才归档当前 batch；gated/blocked 只汇总等待事项，不得启动下一轮 batch-code-scan。",
    "max_ticks 用尽只是本次 runner 配额结束，不是人工 gate。",
  ].join("\n");
}

function runClaudeTick(state) {
  const tick = state.used_ticks + 1;
  const prompt = claudePrompt(tick, state.max_ticks);
  const result = spawnSync("claude", ["-p", prompt], {
    cwd,
    encoding: "utf8",
    maxBuffer: 1024 * 1024 * 20,
  });
  const output = `${result.stdout || ""}${result.stderr ? `\n[stderr]\n${result.stderr}` : ""}`;
  const tokens = logTokens(tick, "loop-tick", prompt, output);
  appendFileSync(runLogPath, `\n## Tick ${tick}\n\n${output.trim() || "(no output)"}\n\n`);
  state.used_ticks = tick;
  state.token_used_estimate = (state.token_used_estimate || 0) + tokens;
  state.updated_at = nowIso();
  state.last_exit_code = result.status;
  if (result.error) state.last_error = String(result.error.message || result.error);
  if (result.status !== 0) state.consecutive_failures = (state.consecutive_failures || 0) + 1;
  else state.consecutive_failures = 0;
  return result.status || 0;
}

function start(maxTicksArg) {
  ensureLoopDir();
  if (existsSync(stopPath)) unlinkSync(stopPath);
  const current = readState();
  const shouldStartNewBatch = current.batch_status === "archived";
  const batchStatus = shouldStartNewBatch
    ? "ready-for-scan"
    : current.batch_status || (current.batch_id ? "active" : "ready-for-scan");
  const state = {
    ...current,
    status: "running",
    batch_status: batchStatus,
    batch_id: shouldStartNewBatch ? defaultBatchId() : current.batch_id || defaultBatchId(),
    max_ticks: parseMaxTicks(maxTicksArg),
    used_ticks: 0,
    token_used_estimate: 0,
    consecutive_failures: 0,
    started_at: nowIso(),
    updated_at: nowIso(),
    cwd,
    runner: "plugins/human-plan/loop/runner.js",
  };
  delete state.stop_reason;
  delete state.last_error;
  delete state.last_exit_code;
  writeState(state);
  logRun(`start max_ticks=${state.max_ticks}`);

  while (state.used_ticks < state.max_ticks) {
    if (existsSync(stopPath)) {
      state.status = "stopped";
      state.updated_at = nowIso();
      writeState(state);
      logRun("stop requested by STOP file");
      break;
    }
    const exitCode = runClaudeTick(state);
    if (state.consecutive_failures >= 3) {
      state.status = "failed";
      writeState(state);
      logRun("stopped after 3 consecutive Claude failures");
      process.exitCode = exitCode;
      return;
    }
    writeState(state);
  }

  if (state.status === "running") {
    state.status = "stopped";
    state.stop_reason = "max_ticks_reached";
    state.updated_at = nowIso();
    writeState(state);
    logRun(`stopped after ${state.used_ticks}/${state.max_ticks} ticks`);
  }
  printStatus();
}

function stop() {
  ensureLoopDir();
  writeFileSync(stopPath, `${nowIso()} stop requested\n`);
  const state = Object.assign({}, readState(), { status: "stopping", updated_at: nowIso() });
  writeState(state);
  logRun("stop requested");
  console.log(`Stop requested: ${resolve(stopPath)}`);
}

function printStatus() {
  ensureLoopDir();
  const state = readState();
  console.log(JSON.stringify(state, null, 2));
  console.log(`\nLoop dir: ${resolve(loopDir)}`);
  console.log(`Run log: ${resolve(runLogPath)}`);
  console.log(`Token ledger: ${resolve(tokenLedgerPath)}`);
}

const command = process.argv[2] || "status";
const arg = process.argv[3];

if (command === "start") start(arg);
else if (command === "stop") stop();
else if (command === "status") printStatus();
else {
  console.error("Usage: node plugins/human-plan/loop/runner.js start [max_ticks] | status | stop");
  process.exit(2);
}
