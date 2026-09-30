export const meta = {
  name: 'boeing-airbus-wargame',
  description: 'Boeing vs Airbus strategy war game: agent teams issue sealed orders each turn, a market cell reacts, the wargame engine adjudicates, then a verified after-action review and report',
  whenToUse: 'Run an AI-vs-AI Boeing vs Airbus war game on the wargame/ engine. Optional args: {turns, scenario, injects: "umpire"|"auto"|"none", games (1-4), run_id, seed, doctrine: {boeing, airbus}, fixed_orders: {boeing|airbus: {"<turn>": orders}}, verify: true|false}',
  phases: [
    { title: 'Setup', detail: 'control cell creates the run(s)' },
    { title: 'Turns', detail: 'inject, sealed Boeing and Airbus orders, market reaction, engine adjudication' },
    { title: 'After-action review', detail: 'equilibria, regret, turning points, checkable claims' },
    { title: 'Verify', detail: 'three independent checks per claim' },
    { title: 'Report', detail: 'report.md per game, plus a cross-game synthesis' },
  ],
}

// ---------------------------------------------------------------------------
// Arguments
// ---------------------------------------------------------------------------

const A = args && typeof args === 'object' && !Array.isArray(args) ? args : {}
const ENGINE = 'python3 -m wargame.engine'
const SCENARIO = typeof A.scenario === 'string' && /^[A-Za-z0-9_-]+$/.test(A.scenario) ? A.scenario : 'base'
const TURNS = Number.isInteger(A.turns) && A.turns > 0 ? A.turns : null
const INJECTS = ['umpire', 'auto', 'none'].includes(A.injects) ? A.injects : 'umpire'
const GAMES = Number.isInteger(A.games) ? Math.max(1, Math.min(4, A.games)) : 1
const SEED = Number.isInteger(A.seed) ? A.seed : 0
const RUN_ID = typeof A.run_id === 'string' && /^[A-Za-z0-9_-]+$/.test(A.run_id) ? A.run_id : null
const DOCTRINE = A.doctrine && typeof A.doctrine === 'object' ? A.doctrine : {}
const FIXED = A.fixed_orders && typeof A.fixed_orders === 'object' ? A.fixed_orders : {}
const VERIFY = A.verify !== false
const MAX_CLAIMS = 8
const SIDES = ['boeing', 'airbus']
const LABEL = { boeing: 'Boeing', airbus: 'Airbus' }

if (Number.isInteger(A.games) && A.games !== GAMES) log(`games clamped to ${GAMES} (allowed 1-4)`)
if (A.scenario && A.scenario !== SCENARIO) log(`ignored invalid scenario '${A.scenario}'; using base`)

// ---------------------------------------------------------------------------
// Schemas
// ---------------------------------------------------------------------------

const launchItem = programs => ({
  type: 'object',
  properties: {
    program: { type: 'string', enum: programs },
    year: { type: 'integer' },
    engine: { type: 'string' },
    variant: { type: 'string', enum: ['solo', 'jv', 'none'] },
  },
  required: ['program', 'year', 'engine', 'variant'],
})

const ORDERS_SCHEMA = {
  boeing: {
    type: 'object',
    properties: {
      launch: { type: 'array', items: launchItem(['fps', 're787']) },
      cancel: { type: 'array', items: { type: 'string', enum: ['fps', 're787'] } },
      rate_increase: { type: 'boolean' },
      public_statement: { type: 'string' },
      rationale: { type: 'string' },
      expected_delta_pv_b: { type: 'number' },
    },
    required: ['launch', 'cancel', 'rate_increase', 'public_statement', 'rationale', 'expected_delta_pv_b'],
  },
  airbus: {
    type: 'object',
    properties: {
      launch: { type: 'array', items: launchItem(['ngsa', 'rea350']) },
      cancel: { type: 'array', items: { type: 'string', enum: ['ngsa', 'rea350'] } },
      delay_tactics: { type: 'boolean' },
      poaching: { type: 'boolean' },
      public_statement: { type: 'string' },
      rationale: { type: 'string' },
      expected_delta_pv_b: { type: 'number' },
    },
    required: ['launch', 'cancel', 'delay_tactics', 'poaching', 'public_statement', 'rationale', 'expected_delta_pv_b'],
  },
}

const SETUP_SCHEMA = {
  type: 'object',
  properties: {
    runs: {
      type: 'array',
      items: {
        type: 'object',
        properties: { run_id: { type: 'string' }, turns_total: { type: 'integer' } },
        required: ['run_id', 'turns_total'],
      },
    },
    turns: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          turn: { type: 'integer' },
          first_year: { type: 'integer' },
          last_year: { type: 'integer' },
          label: { type: 'string' },
        },
        required: ['turn', 'first_year', 'last_year'],
      },
    },
    scenario_title: { type: 'string' },
    error: { type: 'string' },
  },
  required: ['runs', 'turns', 'scenario_title'],
}

const CONTROL_TURN_SCHEMA = {
  type: 'object',
  properties: {
    inject_id: { type: 'string' },
    inject_title: { type: 'string' },
    inject_reason: { type: 'string' },
    situation: { type: 'string' },
    error: { type: 'string' },
  },
  required: ['inject_id', 'situation'],
}

const MARKET_SCHEMA = {
  type: 'object',
  properties: {
    narrative: { type: 'string' },
    reactions: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          program: { type: 'string', enum: ['fps', 're787', 'ngsa', 'rea350'] },
          capture_mult: { type: 'number' },
          reason: { type: 'string' },
        },
        required: ['program', 'capture_mult', 'reason'],
      },
    },
  },
  required: ['narrative', 'reactions'],
}

const ADJ_SCHEMA = {
  type: 'object',
  properties: {
    status: { type: 'string', enum: ['ok', 'invalid', 'error'] },
    boeing_digest: { type: 'string' },
    airbus_digest: { type: 'string' },
    boeing_delta_pv_b: { type: 'number' },
    airbus_delta_pv_b: { type: 'number' },
    boeing_errors: { type: 'array', items: { type: 'string' } },
    airbus_errors: { type: 'array', items: { type: 'string' } },
    game_complete: { type: 'boolean' },
    public_events: { type: 'array', items: { type: 'string' } },
    error: { type: 'string' },
  },
  required: ['status'],
}

const AAR_SCHEMA = {
  type: 'object',
  properties: {
    headline: { type: 'string' },
    final_delta_pv_b: {
      type: 'object',
      properties: { boeing: { type: 'number' }, airbus: { type: 'number' } },
      required: ['boeing', 'airbus'],
    },
    equilibrium_comparison: { type: 'string' },
    regret_b: {
      type: 'object',
      properties: { boeing: { type: 'number' }, airbus: { type: 'number' } },
      required: ['boeing', 'airbus'],
    },
    turning_points: {
      type: 'array',
      items: {
        type: 'object',
        properties: { turn: { type: 'integer' }, what: { type: 'string' }, why_it_mattered: { type: 'string' } },
        required: ['turn', 'what', 'why_it_mattered'],
      },
    },
    claims: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          statement: { type: 'string' },
          command: { type: 'string' },
          expected: { type: 'string' },
        },
        required: ['id', 'statement', 'command', 'expected'],
      },
    },
    lessons: {
      type: 'object',
      properties: {
        boeing: { type: 'array', items: { type: 'string' } },
        airbus: { type: 'array', items: { type: 'string' } },
      },
      required: ['boeing', 'airbus'],
    },
    caveats: { type: 'array', items: { type: 'string' } },
  },
  required: ['headline', 'final_delta_pv_b', 'equilibrium_comparison', 'regret_b', 'turning_points', 'claims', 'lessons', 'caveats'],
}

const VERDICT_SCHEMA = {
  type: 'object',
  properties: {
    upheld: { type: 'boolean' },
    observed: { type: 'string' },
    reason: { type: 'string' },
  },
  required: ['upheld', 'observed', 'reason'],
}

const REPORT_SCHEMA = {
  type: 'object',
  properties: { path: { type: 'string' }, summary: { type: 'string' } },
  required: ['path', 'summary'],
}

const LENSES = [
  {
    key: 'reproduce',
    ask: 'Reproduce the numbers. Run the command exactly, plus any closely related read-only engine command you need. Is every number in the claim what the engine prints, to the stated precision? A claim with a wrong number is refuted.',
  },
  {
    key: 'causal',
    ask: 'Check the causal story. Does the engine output support the claim\'s "because", not just a correlated fact? If the claim is about why something happened, test it with one targeted whatif counterfactual. Refute over-reaching causal claims.',
  },
  {
    key: 'economics',
    ask: 'Check direction and economic sense against the mechanics in `rules`; for example, more strain should never raise a payoff. Is anything left out that would flip the conclusion, such as a counterfactual that held the opponent fixed without saying so? Refute if the claim is misleading.',
  },
]

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const missingTypes = new Set()

// Run a role agent from .claude/agents; fall back to the default agent reading the role card
// (custom agent types written mid-session only register in a later session).
async function call(role, prompt, opts) {
  if (!missingTypes.has(role)) {
    try {
      return await agent(prompt, Object.assign({}, opts, { agentType: role }))
    } catch (e) {
      missingTypes.add(role)
      log(`agent type '${role}' unavailable (${String((e && e.message) || e).slice(0, 120)}); using its role card`)
    }
  }
  return agent(`First read .claude/agents/${role}.md and follow the instructions below its YAML header as your role for this task.\n\n${prompt}`, opts)
}

// 32-bit FNV-1a, mirrored in wargame/model.py (orders_digest).
function fnv1a(s) {
  let h = 0x811c9dc5
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i) & 0xff
    h = Math.imul(h, 0x01000193) >>> 0
  }
  return (h >>> 0).toString(16).padStart(8, '0')
}

// Mirrors wargame/model.py canonical_key for the payload built by enginePayload.
function canonKey(side, o) {
  const launches = (o.launch || [])
    .slice()
    .sort((x, y) => (x.program < y.program ? -1 : x.program > y.program ? 1 : 0))
    .map(L => `${L.program}/${L.variant || '-'}/${L.engine}/${L.year}`)
    .join(';')
  const cancels = Array.from(new Set(o.cancel || [])).sort().join(',')
  const flags = side === 'boeing' ? ['rate_increase'] : ['delay_tactics', 'poaching']
  return `${side}|L=${launches}|C=${cancels}|F=${flags.map(f => `${f}:${o[f] ? 1 : 0}`).join(',')}`
}

function clean(s) {
  return String(s == null ? '' : s).split('WARGAME_EOF').join('WARGAME-EOF')
}

// Orders exactly as the engine will see them. fps always carries an explicit variant.
function enginePayload(side, o) {
  const p = {
    launch: (o.launch || []).map(L => {
      const e = { program: L.program, year: L.year, engine: L.engine }
      const v = L.variant && L.variant !== 'none' ? L.variant : L.program === 'fps' ? 'solo' : null
      if (v) e.variant = v
      return e
    }),
    cancel: Array.from(new Set(o.cancel || [])),
    public_statement: clean(o.public_statement),
    rationale: clean(o.rationale),
  }
  if (side === 'boeing') p.rate_increase = !!o.rate_increase
  else {
    p.delay_tactics = !!o.delay_tactics
    p.poaching = !!o.poaching
  }
  return p
}

function publicPart(side, o) {
  const p = { launch: o.launch || [], cancel: o.cancel || [], public_statement: o.public_statement || '' }
  if (side === 'boeing') p.rate_increase = !!o.rate_increase
  else p.poaching = !!o.poaching // Delay Tactics are covert and never shown
  return p
}

function describe(side, o) {
  const parts = (o.launch || []).map(L => `launch ${L.program}${L.variant && L.variant !== 'none' ? ' ' + L.variant : ''} ${L.year}`)
  ;(o.cancel || []).forEach(p => parts.push(`cancel ${p}`))
  if (side === 'boeing' && o.rate_increase) parts.push('rate increase')
  if (side === 'airbus' && o.delay_tactics) parts.push('Delay Tactics')
  if (side === 'airbus' && o.poaching) parts.push('Poaching')
  return parts.length ? parts.join(' + ') : 'no new moves'
}

function fmt(x) {
  return typeof x === 'number' ? (x >= 0 ? '+' : '') + x.toFixed(2) : '?'
}

// ---------------------------------------------------------------------------
// Prompts
// ---------------------------------------------------------------------------

function setupPrompt() {
  const suffix = i => (GAMES > 1 ? `-g${i}` : '')
  const prefix = RUN_ID || 'wg-<timestamp>'
  const cmds = []
  for (let i = 1; i <= GAMES; i++) {
    cmds.push(`${ENGINE} new --run-id ${prefix}${suffix(i)} --scenario ${SCENARIO}${TURNS ? ' --turns ' + TURNS : ''} --seed ${SEED + i - 1}`)
  }
  return [
    `Create ${GAMES} Boeing vs Airbus war game run(s) with the wargame engine. You are control.`,
    RUN_ID ? '' : 'First get a timestamp with `date +%Y%m%d-%H%M%S` and substitute it for <timestamp> below.',
    'Run:\n```bash\n' + cmds.join('\n') + '\n```',
    'If a command fails (for example the run id already exists or the scenario or turn count is invalid), stop and put the exact error in `error`.',
    'Return: runs (run_id and turns_total for each), the turns list from the `new` output (turn, first_year, last_year, label), and the scenario title.',
  ].filter(Boolean).join('\n\n')
}

function controlTurnPrompt(g, t) {
  const inj =
    INJECTS === 'umpire'
      ? `Inject policy "umpire": run \`${ENGINE} injects --run ${g.runId}\`. Choose at most one inject, or quiet_turn, that best stress-tests the strategies now in play. Apply it with \`${ENGINE} inject --run ${g.runId} --id <id>\` and give a one-sentence reason.`
      : INJECTS === 'auto'
        ? `Inject policy "auto": run \`${ENGINE} inject --run ${g.runId} --auto\`.`
        : `Inject policy "none": run \`${ENGINE} inject --run ${g.runId} --none\`.`
  return [
    `War game run \`${g.runId}\`, turn ${t} of ${g.turnsTotal}. You are control.`,
    `1. Run \`${ENGINE} status --run ${g.runId}\` and confirm the run is on turn ${t}. If it is not, stop and report the mismatch in \`error\`.`,
    `2. ${inj}`,
    `3. Run \`${ENGINE} brief --run ${g.runId} --side market\` to get the public view.`,
    `4. Write a public situation report of at most 150 words. Cover the turn and its years, this turn's inject, which programs have been launched, cancelled or slipped (with EIS dates), last turn's public statements, and the market's last reaction. Use only facts from that public brief: no projections, nothing private or covert.`,
    'Return inject_id (or "none"), inject_title, inject_reason and situation.',
  ].join('\n')
}

function playerPrompt(g, t, side, ctl, errors) {
  const ty = g.years[t]
  const variantRule = side === 'boeing' ? '"solo" or "jv" for fps, "none" for re787' : '"none"'
  return [
    `War game run \`${g.runId}\`. You are ${LABEL[side]}. This is turn ${t} of ${g.turnsTotal} (${ty.first_year}-${ty.last_year}${ty.label ? ', ' + ty.label : ''}).`,
    `Follow your role instructions. Read your behavioural profile (wargame/profiles/${side}/profile.md, starting with the Quick card), then run brief, rules (on turn 1), options, whatif and validate, and return your orders. Always pass \`--run ${g.runId} --side ${side}\`.`,
    `Control's public situation report:\n${ctl.situation}`,
    DOCTRINE[side] ? `Board guidance for this game. Treat it as a real constraint on your decisions: ${DOCTRINE[side]}` : '',
    errors && errors.length ? `The engine rejected your previous orders for this turn:\n- ${errors.join('\n- ')}\nFix them, re-run validate, and resubmit.` : '',
    `Every launch entry needs program, year (${ty.first_year}-${ty.last_year}), engine and variant (${variantRule}). Put the engine numbers you relied on in the rationale. Put the engine's projected delta PV for these orders, assuming no later moves, in expected_delta_pv_b.`,
  ]
    .filter(Boolean)
    .join('\n\n')
}

function marketPrompt(g, t, orders, ctl) {
  const pub = SIDES.map(s => `${LABEL[s]}: ${JSON.stringify(publicPart(s, orders[s]))}`).join('\n')
  return [
    `War game run \`${g.runId}\`, turn ${t}. You are the market cell.`,
    `Read the public view: \`${ENGINE} brief --run ${g.runId} --side market\`. Add \`${ENGINE} rules --run ${g.runId} --side market\` if you need the mechanics.`,
    `This turn's public moves, announced at the same time:\n${pub}`,
    `Control's situation report:\n${ctl.situation}`,
    'Return your market narrative and capture_mult reactions for launched programs, including ones launched this turn (program ids: fps, re787, ngsa, rea350). Leave out programs whose multiplier you keep unchanged.',
  ].join('\n\n')
}

function adjudicatePrompt(g, t, cmd, retry) {
  return [
    `War game run \`${g.runId}\`, turn ${t}. You are control. Adjudicate this turn by running the command below in a single Bash call, EXACTLY as written: copy it byte for byte. It is a quoted heredoc, so do not re-type, reformat or edit the JSON.`,
    retry ? 'An earlier attempt failed. Run the command verbatim.' : '',
    '```bash\n' + cmd + '\n```',
    'Report from the engine output:',
    '- status: "ok"; "invalid" if the engine printed status "invalid"; otherwise "error".',
    '- orders_digest values, as boeing_digest and airbus_digest.',
    '- projection delta_pv_b per side, as boeing_delta_pv_b and airbus_delta_pv_b.',
    '- game_complete, and the text of this turn\'s public events.',
    '- For "invalid": the per-side error lists (boeing_errors, airbus_errors).',
    '- For "error": the exact error text, in error.',
  ]
    .filter(Boolean)
    .join('\n\n')
}

function aarPrompt(g, expectations) {
  return [
    `After-action review of completed war game run \`${g.runId}\`. Scenario ${SCENARIO}, ${g.turnsTotal} turns, inject policy ${INJECTS}${DOCTRINE.boeing || DOCTRINE.airbus ? ', board guidance ' + JSON.stringify(DOCTRINE) : ''}.`,
    `Run \`${ENGINE} report --run ${g.runId}\`, \`${ENGINE} equilibria --run ${g.runId} --from-turn 1\`, and the narrowbody and widebody sub-games (\`--segment nb\`, \`--segment wb\`). Use \`${ENGINE} whatif --run ${g.runId} --side analyst\` for the counterfactuals behind your turning points.`,
    `Each side's engine-projected delta PV at the moment it ordered (assuming no later moves), per turn:\n${expectations}`,
    'Produce:',
    '- a one-sentence headline;',
    '- final delta PV per side;',
    '- how actual play compares with the pure and near-Nash plans, with each side\'s regret (from regret_vs_actual);',
    '- 2-5 turning points;',
    '- 2-4 lessons for each side;',
    '- model caveats;',
    `- at most ${MAX_CLAIMS} checkable claims: the load-bearing facts of your review. Each claim has an id (C1, C2, ...), a one-sentence statement, the exact engine command that shows it (runnable as-is, with a heredoc for whatif), and the value(s) that command should print.`,
  ].join('\n\n')
}

function verifyPrompt(g, c, lens) {
  return [
    `You independently check one claim from the after-action review of war game run \`${g.runId}\`. The engine is \`${ENGINE}\`; see wargame/README.md.`,
    'Use only read-only engine commands: report, equilibria, whatif --side analyst, brief --side analyst, rules. Never run new, inject, adjudicate or rollback. Never edit files.',
    `Claim ${c.id}: ${c.statement}`,
    `Evidence offered: \`${c.command}\` should show: ${c.expected}`,
    `Your lens (${lens.key}): ${lens.ask}`,
    'If engine output does not confirm the claim, answer upheld=false. Report what you observed, with numbers exactly as printed, and why.',
  ].join('\n\n')
}

function reportPrompt(g, aar, verified, refuted, dropped, expectations) {
  return [
    `Write the report for completed war game run \`${g.runId}\` to \`wargame/runs/${g.runId}/report.md\` (Markdown), then return its path and a three-sentence summary.`,
    'Structure:',
    '1. Title and a short headline paragraph. Use only verified facts.',
    `2. Setup: scenario ${SCENARIO}, ${g.turnsTotal} turns, inject policy ${INJECTS}${DOCTRINE.boeing || DOCTRINE.airbus ? ', board guidance ' + JSON.stringify(DOCTRINE) : ''}.`,
    `3. Engine tables: paste the output of \`${ENGINE} report --run ${g.runId} --format md\` verbatim. Do not retype the numbers.`,
    `4. Turn-by-turn narrative from \`${ENGINE} report --run ${g.runId}\`: the inject, what each side did and why (from their rationales), the market reaction, and the projection change.`,
    '5. Equilibrium benchmark and regret.',
    '6. Turning points.',
    '7. Lessons for Boeing and for Airbus.',
    '8. Verified claims, each with its command and the checkers\' vote.',
    '9. Appendix: claims that failed verification or were not checked, with their votes. Nothing is silently dropped.',
    '10. Model caveats, separating CALIBRATED from PLACEHOLDER parameters (see wargame/README.md).',
    `Expectations at order time:\n${expectations}`,
    `After-action review (JSON):\n${JSON.stringify(aar, null, 1)}`,
    `Verified claims (JSON):\n${JSON.stringify(verified, null, 1)}`,
    `Refuted claims (JSON):\n${JSON.stringify(refuted, null, 1)}`,
    dropped.length ? `Claims not checked because of the ${MAX_CLAIMS}-claim cap (JSON):\n${JSON.stringify(dropped, null, 1)}` : '',
  ]
    .filter(Boolean)
    .join('\n\n')
}

function synthesisPrompt(done, path) {
  return [
    `Write a cross-game synthesis of ${done.length} independent plays of the same Boeing vs Airbus war game to \`${path}\` (Markdown), then return its path and a three-sentence summary.`,
    `Runs: ${done.map(d => `\`${d.run_id}\` (report: ${d.report_path})`).join(', ')}.`,
    `Read each report.md and \`${ENGINE} report --run <id>\`. Compare decisions and outcomes across games: which choices were robust and which depended on injects or on the other side's play. Use a table of final delta PV per side per game, taken from engine output. Give conclusions for Boeing and for Airbus, and note where the games disagreed.`,
  ].join('\n\n')
}

// ---------------------------------------------------------------------------
// Game loop
// ---------------------------------------------------------------------------

function fixedOrdersFor(g, side, t) {
  const bySide = FIXED[side]
  if (!bySide || typeof bySide !== 'object') return null
  const o = bySide[String(t)] || bySide[t]
  if (!o) return null
  const ty = g.years[t]
  const launch = (o.launch || []).map(L => {
    const e = typeof L === 'string' ? { program: L } : Object.assign({}, L)
    if (!e.engine) throw new Error(`fixed_orders.${side}.${t}: launch of ${e.program} needs an engine`)
    return {
      program: e.program,
      year: Number.isInteger(e.year) ? e.year : ty.first_year,
      engine: e.engine,
      variant: e.variant || (e.program === 'fps' ? 'solo' : 'none'),
    }
  })
  const out = {
    launch,
    cancel: o.cancel || [],
    public_statement: o.public_statement || '',
    rationale: o.rationale || 'Scripted orders (fixed_orders argument).',
    expected_delta_pv_b: 0,
    scripted: true,
  }
  if (side === 'boeing') out.rate_increase = !!o.rate_increase
  else {
    out.delay_tactics = !!o.delay_tactics
    out.poaching = !!o.poaching
  }
  return out
}

async function sideOrders(g, t, side, ctl, errors) {
  const fixed = fixedOrdersFor(g, side, t)
  if (fixed) {
    if (errors && errors.length) throw new Error(`${g.tag}fixed_orders for ${side} turn ${t} are invalid: ${errors.join('; ')}`)
    return fixed
  }
  const r = await call(`${side}-strategist`, playerPrompt(g, t, side, ctl, errors), {
    label: `${g.tag}T${t} ${LABEL[side]}${errors ? ' (fix)' : ''}`,
    phase: 'Turns',
    schema: ORDERS_SCHEMA[side],
  })
  if (!r) throw new Error(`${g.tag}${LABEL[side]} returned no orders for turn ${t}`)
  return r
}

async function adjudicate(g, t, orders, market, retry) {
  const payload = {
    boeing: enginePayload('boeing', orders.boeing),
    airbus: enginePayload('airbus', orders.airbus),
    market: { narrative: clean(market.narrative), capture_mult: {} },
  }
  for (const r of market.reactions || []) payload.market.capture_mult[r.program] = r.capture_mult
  const digests = {}
  SIDES.forEach(s => (digests[s] = fnv1a(canonKey(s, payload[s]))))
  const cmd =
    `${ENGINE} adjudicate --run ${g.runId} --turn ${t} --expect-digest boeing=${digests.boeing},airbus=${digests.airbus} <<'WARGAME_EOF'\n` +
    `${JSON.stringify(payload, null, 1)}\nWARGAME_EOF`
  const r = await call('wargame-control', adjudicatePrompt(g, t, cmd, retry), {
    label: `${g.tag}T${t} adjudicate${retry ? ' (retry)' : ''}`,
    phase: 'Turns',
    schema: ADJ_SCHEMA,
  })
  const res = r || { status: 'error', error: 'control returned nothing' }
  res.expected_digests = digests
  return res
}

async function playGame(g) {
  const turns = []
  for (let t = 1; t <= g.turnsTotal; t++) {
    const ctl = await call('wargame-control', controlTurnPrompt(g, t), {
      label: `${g.tag}T${t} control`,
      phase: 'Turns',
      schema: CONTROL_TURN_SCHEMA,
    })
    if (!ctl || ctl.error) throw new Error(`${g.tag}turn ${t} control failed: ${(ctl && ctl.error) || 'no result'}`)
    log(`${g.tag}T${t} inject: ${ctl.inject_title || ctl.inject_id}`)

    const orders = {}
    const got = await parallel(SIDES.map(side => () => sideOrders(g, t, side, ctl, null)))
    SIDES.forEach((s, i) => (orders[s] = got[i]))
    SIDES.forEach(s => {
      if (!orders[s]) throw new Error(`${g.tag}${LABEL[s]} failed to order in turn ${t}`)
    })

    const market = (await call('wargame-market', marketPrompt(g, t, orders, ctl), {
      label: `${g.tag}T${t} market`,
      phase: 'Turns',
      schema: MARKET_SCHEMA,
    })) || { narrative: '', reactions: [] }

    let adj = await adjudicate(g, t, orders, market, false)
    if (adj.status === 'invalid') {
      const fixed = await parallel(
        SIDES.map(side => () => {
          const errs = adj[`${side}_errors`] || []
          return errs.length ? sideOrders(g, t, side, ctl, errs) : Promise.resolve(orders[side])
        }),
      )
      SIDES.forEach((s, i) => {
        if (fixed[i]) orders[s] = fixed[i]
      })
      adj = await adjudicate(g, t, orders, market, false)
    } else if (adj.status === 'error') {
      adj = await adjudicate(g, t, orders, market, true)
    }
    if (adj.status !== 'ok') {
      throw new Error(`${g.tag}turn ${t} adjudication failed: ${adj.error || JSON.stringify(adj.boeing_errors || adj.airbus_errors || adj)}`)
    }
    SIDES.forEach(s => {
      const got = adj[`${s}_digest`]
      if (got && got !== adj.expected_digests[s]) {
        log(`${g.tag}T${t} WARNING: control reported ${s} digest ${got}, expected ${adj.expected_digests[s]} (the engine enforces the digest, so this is probably a transcription slip in the report)`)
      }
    })
    log(
      `${g.tag}T${t}: Boeing ${describe('boeing', orders.boeing)} | Airbus ${describe('airbus', orders.airbus)} | projected $B: Boeing ${fmt(adj.boeing_delta_pv_b)}, Airbus ${fmt(adj.airbus_delta_pv_b)}`,
    )
    turns.push({
      turn: t,
      inject: ctl.inject_title || ctl.inject_id,
      orders: { boeing: describe('boeing', orders.boeing), airbus: describe('airbus', orders.airbus) },
      expected: { boeing: orders.boeing.expected_delta_pv_b, airbus: orders.airbus.expected_delta_pv_b },
      projected: { boeing: adj.boeing_delta_pv_b, airbus: adj.airbus_delta_pv_b },
    })
  }

  const expectations = turns
    .map(x => `T${x.turn}: Boeing expected ${fmt(x.expected.boeing)}, Airbus expected ${fmt(x.expected.airbus)} ($B)`)
    .join('\n')

  const aar = await call('wargame-analyst', aarPrompt(g, expectations), {
    label: `${g.tag}AAR`,
    phase: 'After-action review',
    schema: AAR_SCHEMA,
  })
  if (!aar) throw new Error(`${g.tag}after-action review failed`)
  const claims = (aar.claims || []).slice(0, MAX_CLAIMS)
  const dropped = (aar.claims || []).slice(MAX_CLAIMS)
  if (dropped.length) log(`${g.tag}${dropped.length} claim(s) beyond the ${MAX_CLAIMS}-claim cap are listed as unchecked in the report`)

  const verified = []
  const refuted = []
  if (VERIFY && claims.length) {
    const checked = await parallel(
      claims.map(c => () =>
        parallel(
          LENSES.map(lens => () =>
            agent(verifyPrompt(g, c, lens), { label: `${g.tag}check ${c.id} ${lens.key}`, phase: 'Verify', schema: VERDICT_SCHEMA }),
          ),
        ).then(vs => ({ c, vs: vs.filter(Boolean) })),
      ),
    )
    for (const r of checked.filter(Boolean)) {
      const up = r.vs.filter(v => v.upheld).length
      const entry = Object.assign({}, r.c, {
        votes: `${up}/${LENSES.length} upheld${r.vs.length < LENSES.length ? ` (${LENSES.length - r.vs.length} checker(s) failed)` : ''}`,
        checker_notes: r.vs.map(v => `${v.upheld ? 'upheld' : 'refuted'}: ${v.reason}`),
      })
      ;(up >= 2 ? verified : refuted).push(entry)
    }
    log(`${g.tag}claims: ${verified.length} verified, ${refuted.length} refuted`)
  } else if (!VERIFY) {
    claims.forEach(c => dropped.push(c))
    claims.length = 0
    log(`${g.tag}verification skipped (verify: false); all claims reported as unchecked`)
  }

  const rep = await call('wargame-analyst', reportPrompt(g, aar, verified, refuted, dropped, expectations), {
    label: `${g.tag}report`,
    phase: 'Report',
    schema: REPORT_SCHEMA,
  })
  return {
    run_id: g.runId,
    headline: aar.headline,
    final_delta_pv_b: aar.final_delta_pv_b,
    regret_b: aar.regret_b,
    turns,
    verified_claims: verified.length,
    refuted_claims: refuted.length,
    unchecked_claims: dropped.length,
    report_path: rep ? rep.path : null,
    report_summary: rep ? rep.summary : null,
  }
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

phase('Setup')
const setup = await call('wargame-control', setupPrompt(), { label: 'setup', phase: 'Setup', schema: SETUP_SCHEMA })
if (!setup || setup.error || !setup.runs || !setup.runs.length) {
  throw new Error(`setup failed: ${(setup && setup.error) || 'no runs created'}`)
}
const years = {}
for (const t of setup.turns) years[t.turn] = t
const games = setup.runs.map((r, i) => ({
  index: i + 1,
  runId: r.run_id,
  turnsTotal: r.turns_total,
  years,
  tag: setup.runs.length > 1 ? `G${i + 1} ` : '',
}))
for (const g of games) {
  for (let t = 1; t <= g.turnsTotal; t++) {
    if (!years[t]) throw new Error(`setup did not return the years of turn ${t}`)
  }
}
log(`${games.length} game(s): ${games.map(g => g.runId).join(', ')} (${setup.scenario_title}, ${games[0].turnsTotal} turns, injects: ${INJECTS})`)

phase('Turns')
const results = await parallel(
  games.map(g => async () => {
    try {
      return await playGame(g)
    } catch (e) {
      log(`${g.tag}game ${g.runId} stopped: ${String((e && e.message) || e)}`)
      return { run_id: g.runId, error: String((e && e.message) || e) }
    }
  }),
)

let synthesis = null
const done = results.filter(r => r && !r.error && r.report_path)
if (done.length > 1) {
  phase('Report')
  const path = `wargame/runs/${done[0].run_id.replace(/-g\d+$/, '')}-synthesis.md`
  synthesis = await call('wargame-analyst', synthesisPrompt(done, path), { label: 'synthesis', phase: 'Report', schema: REPORT_SCHEMA })
}

return {
  scenario: SCENARIO,
  inject_policy: INJECTS,
  games: results,
  synthesis: synthesis ? synthesis.path : null,
}
