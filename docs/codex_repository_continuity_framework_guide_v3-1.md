# Codex Repository Continuity Framework Guide v3.1

긴 작업의 목표와 판단을 여러 세션에 걸쳐 보존하되, 얕은 시작 구조와 저비용 주기 관리를 유지하는 범용 프레임

## 1. 해결하려는 문제

이 프레임은 특정 연구 workflow나 거대한 multi-agent 운영체제를 강제하지 않는다. 해결 대상은 더 일반적이다.

> 긴 작업을 여러 세션으로 나눠도 Codex가 장기 목표, 현재 판단 지점, 검증 근거, 이미 배운 제약을 잊지 않고 이어가게 한다.

반복 작업에서는 다음 drift가 흔하다.

```text
원래 목표
  -> 작은 작업 또는 실험
  -> 부분 성과나 실패
  -> local metric과 새 아이디어 추가
  -> scope와 복잡성 증가
  -> 원래 성공 기준 상실
```

이는 단순한 chat memory 부족만이 아니라 goal drift, handoff 손실, 검증 discipline의 문제다. 해결책은 모든 대화를 보존하는 것이 아니라 다음 세션에 필요한 정보를 역할별로 분리하는 것이다.

## 2. 설계 원칙

### 얕은 시작점

Root agent는 최초 전파와 최종 통합 노드다. 시작할 때 여러 문서 계층을 순회하지 않고 `AGENTS.md -> GOAL.md -> CURRENT.md -> INDEX.md`에서 필요한 세부 파일로 이동한다.

### 현재 상태와 장기 기억의 분리

- Current state는 지금 이어서 할 일과 현재 판단을 보존한다.
- Durable memory는 미래 행동을 바꾸는 검증된 지식만 보존한다.
- Git과 raw artifacts는 상세 연대기와 원자료를 보존한다.

### 행동 상태기계 대신 주기적 위생 관리

Agent를 여러 mode로 자동 전환하는 복잡한 장치를 두지 않는다. 비-LLM 코드가 상태 변경이 있었던 Codex 턴을 세고, 짧은 주기로 memory maintenance를, 더 긴 주기로 independent review를 알린다.

### 단일 운영 프레임

```text
Continuity
goal + current + active state + memory + cadence + drift review
```

운영 레벨은 하나다. 이전 architecture extension은 역사적 archive로만 보존하며, 문제가 생겨도 자동으로 활성화하거나 승격하지 않는다.

## 3. Level 1 구조

```text
repo/
├── AGENTS.md
├── GOAL.md
├── state/
│   ├── CURRENT.md
│   ├── cadence.json
│   └── active/
│       ├── _template.md
│       └── <task>.md
├── memory/
│   ├── INDEX.md
│   └── records/
│       ├── _template.md
│       └── MEM-0001-*.md
├── .agents/skills/
│   ├── initialize-project-continuity/
│   │   ├── SKILL.md
│   │   └── agents/openai.yaml
│   └── maintain-project-memory/SKILL.md
├── .codex/
│   ├── hooks.json
│   └── agents/drift-reviewer.toml
└── scripts/continuity
```

파일 수는 이전의 네 파일보다 늘었지만 사람이 매번 읽는 context는 늘지 않는다. `CURRENT.md`와 `INDEX.md`가 세부 상태와 memory를 조건부로 연결하기 때문이다. 기계 상태와 실행 절차는 사람용 문서에 섞지 않고 각각 JSON, script, Skill에 둔다.

## 4. Root AGENTS.md

Root `AGENTS.md`는 모든 에이전트의 상세 판단을 담는 문서가 아니다. 다음 기본 의사결정 순서와 최초 전파 규칙만 제공한다.

1. 사용자가 소유한 장기 기준을 읽는다.
2. 현재 primary task와 다음 행동을 찾는다.
3. 관련 memory만 선택한다.
4. 최소한의 coherent action을 정의한다.
5. 구현 또는 조사를 수행하고 근거를 만든다.
6. 현재 snapshot과 memory candidate를 갱신한다.
7. due 신호가 있을 때만 maintenance나 review를 실행한다.

Root에는 새 코드를 만들 때 cohesive module, 명시적 input/output, 가정적 layer 금지라는 최소 원칙만 둔다. 별도의 Coder agent를 기본 실행 경로에 넣지 않는다.

Root가 ordinary implementation과 investigation을 직접 수행한다. 별도 agent는 장기 cadence가 요구하는 fresh read-only drift reviewer 하나만 기본 경로에 있으며, reviewer는 다른 agent를 만들지 않는다.

### 기존 AGENTS.md와 병합

프레임의 `AGENTS.md`는 별도 agent가 아니라 project instruction template이다. 기존 프로젝트에서는 continuity marker block만 root instruction에 병합한다.

```text
기존 project rules + continuity managed block
                    ↓
             root AGENTS.md 하나
```

같은 디렉터리에 두 번째 임의 파일을 만들어도 자동으로 합쳐지지 않는다. 특히 `AGENTS.override.md`가 있으면 그 위치의 `AGENTS.md` 대신 override 하나가 선택되므로 installer는 auto mode에서 중단하고 사용자의 명시적 선택을 요구한다.

### 비대한 AGENTS.md 처리

Codex의 기본 project instruction budget은 root부터 current working directory까지 합쳐 32 KiB다. Root에는 항상 필요한 규칙과 routing만 남긴다.

- 작업 절차는 `.agents/skills`로 이동해 필요할 때만 본문을 load한다.
- 현재 상태는 `CURRENT`와 active state로 이동한다.
- 누적 지식은 조건부 memory record로 이동한다.
- formatting과 기계적 규칙은 formatter, linter, tests, CI로 이동한다.
- 긴 설명과 예시는 일반 문서에 두고 Skill이나 memory에서 연결한다.
- subtree 전용 규칙은 짧은 local `AGENTS.md`에 두고 해당 경로에서 Codex를 시작한다.

여러 instruction 파일로 이름만 나누는 것은 해결책이 아니다. 같은 디렉터리에서는 하나만 선택되며, 하위 파일도 해당 working-directory chain에 들어올 때만 적용된다. `install-continuity --dry-run`은 가장 큰 project chain을 계산해 75%에서 경고하고 설정된 한도를 넘으면 변경 전에 중단한다.

## 5. 초기 continuity 기준선

Generic template을 그대로 방치하면 처음 채워진 표현과 분류가 이후 세션의 관성이 된다. 설치 직후 `$initialize-project-continuity`를 명시적으로 한 번 실행해 프로젝트별 기준선을 만든다.

Skill은 README, manifests, entry points, tests, CI, 기존 project instructions 같은 primary evidence를 조사한다. 코드에서 확인할 수 없는 실제 목적과 성공 기준은 사용자에게 묻는다. 그 결과로 user-owned `GOAL.md`, primary task 하나를 가리키는 `CURRENT.md`, 첫 active state, 필요할 때만 최소 memory record를 만든다.

초기화는 다음을 만들지 않는다.

- 추측성 architecture와 module map
- 여러 speculative active tasks
- 근거를 채우기 위한 memory
- Coder를 포함한 custom agents
- 사용자가 요청하지 않은 project-specific Skills

`CURRENT.md`의 `Continuity baseline`이 `established YYYY-MM-DD`이면 초기화 Skill은 자동으로 재작성하지 않는다. Rebaseline은 사용자가 명시적으로 요청해야 하며, `GOAL.md`의 material change는 다시 사용자 결정을 받는다. 기존 cadence와 memory를 reset하지 않는다.

이 Skill은 `allow_implicit_invocation: false`이므로 ordinary work 중 자동 선택되지 않는다. 초기 문서 생성이 끝나면 기존 continuity 흐름만 사용한다.

## 6. GOAL.md

`GOAL.md`는 사용자 소유 policy다. Codex는 명시적 요청 없이 수정하지 않는다.

포함 항목은 다음과 같다.

- Objective
- Success Criteria
- Guardrails
- Non-Goals and Invalid Shortcuts
- Stopping Conditions
- Current Direction
- Fixed Assumptions

분야별 의미는 프로젝트가 정한다. 예를 들어 실험 프로젝트의 고정 데이터 분할, 제품 프로젝트의 호환성 기준, 마이그레이션 프로젝트의 rollback 조건이 모두 같은 `Fixed Assumptions` 또는 `Guardrails`에 들어갈 수 있다.

Evidence가 목표 변경을 시사하면 active state에 제안하고 사용자가 결정한다. Agent가 local metric이나 편한 산출물을 성공 기준으로 바꾸지 않는다.

## 7. CURRENT와 active state

`state/CURRENT.md`는 하나의 사용자 가독형 router다.

- primary task
- primary active-state path
- 현재 위치를 나타내는 짧은 summary
- 바로 다음 concrete action
- 당장 위반하기 쉬운 constraint
- 다른 active work 링크

`state/active/<task>.md`는 각 작업의 최신 snapshot이다.

```text
Outcome
Goal Connection
Current State
Decisions and Rationale
Evidence
Next Action
Do Not
Memory Candidates
Verification
```

의미 있는 milestone, 판단·근거·scope 변경, handoff 때 갱신한다. 모든 command나 대화 내용을 쌓는 일지는 만들지 않는다. 새 세션이 chat history 없이 같은 판단 지점에서 시작할 정도면 충분하다.

여러 작업이 있어도 시작 노드는 `CURRENT.md` 한 개다. Primary task 하나를 명시하고 나머지는 링크만 둔다.

## 8. 범용 durable memory

Memory는 연구 ledger로 고정하지 않는다. 다음 여섯 유형이 공통 형식으로 공존한다.

- `decision`: 선택과 그 이유
- `lesson`: 재사용할 수 있는 배움
- `failure`: 반복하지 않아야 할 접근과 조건
- `constraint`: 미래 작업이 지켜야 할 경계
- `assumption`: 결과나 판단이 의존하는 전제
- `finding`: 검증된 현상이나 구조적 사실

각 `MEM-*` 레코드는 다음을 포함한다.

```text
ID / Type / Status / Scope / Authority / Trigger / Summary / Last validated
Claim / Evidence / Implication / Does Not Apply / Supersedes / Revalidate When
```

핵심은 `Scope`, `Trigger`, `Does Not Apply`다. 이 필드가 memory를 무조건 모두 읽는 전역 규칙이 아니라 조건부 context로 만든다.

Status는 `active`, `disputed`, `superseded`, `archived`다. 충돌하는 근거가 생기면 즉시 덮어쓰지 않고 disputed로 표시한다. 새 판단이 기존 판단을 대체하면 연결을 남기고 superseded로 전환한다. 오래됐다는 이유만으로 archive하지 않는다.

`memory/INDEX.md`는 script가 생성하며 archived record를 제외한다. ID, type, scope, status, load trigger, summary만 보여 주므로 agent가 필요한 원문만 선택할 수 있다.

## 9. Memory maintenance Skill

진행 중 발견은 우선 active state의 `Memory Candidates`에 둔다. `$maintain-project-memory`는 다음 조건 중 하나일 때 사용한다.

- cadence가 due를 알린다.
- 큰 handoff나 phase 종료가 발생한다.
- 중요한 결정, 비싼 발견, 반복 실패, memory conflict가 생긴다.

Skill은 candidate를 durable memory로 승격할지 선별하고, 중복·충돌·supersession을 정리하며, active state의 candidate를 해소한다. 일상 note나 진행 상황은 승격하지 않는다.

완료 명령은 다음과 같다.

```bash
./scripts/continuity memory-complete
```

이 명령은 index를 다시 만들고 record를 검증하며 memory counter를 초기화하고 review counter를 한 단계 올린다.

## 10. 비-LLM cadence

`scripts/continuity`는 Python 표준 라이브러리만 사용한다. 기본 설정은 다음과 같다.

```json
{
  "memory_every_changed_turns": 3,
  "review_every_memory_runs": 5
}
```

이전 v1의 `memory_every_changed_sessions`와 `changed_sessions_since_memory`는 새 script가 처음 상태를 저장할 때 기존 값을 보존한 채 turn 기반 v2 키로 옮긴다.

이 cadence의 단위는 session이 아니라 `사용자 프롬프트 1회 -> Codex 작업 -> 최종 응답 1회`로 이루어진 턴이다. `Stop`에서 `CURRENT.md`와 active-state 파일들의 hash를 이전 값과 비교하고, hash가 달라진 턴만 memory counter를 올린다. 성공한 `Stop` command는 `{"continue": true}`를 출력한다. command 수나 token 수를 세지 않는다.

다음 `UserPromptSubmit`에서는 due flag가 있을 때만 짧은 `additionalContext`를 출력한다. `SessionStart`는 최초 시작과 resume 때 같은 due 상태를 확인하고, 이전 턴의 `Stop`이 누락됐다면 저장된 hash와 비교해 한 번 복구한다. `SessionEnd`도 마지막 reconciliation을 위한 보조 경로이며 정상 카운트의 기준이 아니다. 저장 hash를 즉시 갱신하므로 여러 복구 경로가 같은 변경을 중복 집계하지 않는다. Script는 내용을 요약하거나 판단하지 않으므로 모델 호출 비용이 없다.

이 방식은 완벽한 의미론적 측정이 아니라 의도적으로 저렴한 근사치다. State를 갱신하지 않은 중요한 작업은 애초에 handoff 규칙 위반이므로 단순 hash가 그 문제도 드러낸다.

시간 기반 scheduled task는 repository가 닫힌 동안에도 실행할 필요가 있는 외부 운영에는 적합하지만, 여기서는 실제 작업량과 분리된다. 따라서 기본 cadence는 달력 시간이 아니라 changed turn 수를 사용한다.

## 11. Fresh independent review

기본적으로 memory maintenance 5회마다 drift review가 due가 된다. Review는 상주 process가 아니라 root가 그 시점에 fresh `drift_reviewer` subagent를 한 번 만들고 보고를 회수하는 작업이다.

가능하면 reviewer에게 구현 대화의 결론을 길게 전달하지 않는다. 대신 다음 원자료와 질문을 전달한다.

- 최초 사용자 outcome과 `GOAL.md`
- `CURRENT.md`와 관련 active state
- 관련 memory records
- primary code, tests, 결과, 로그
- 목표 대체, 실패 반복, scope growth, stale memory 여부

Reviewer는 read-only이고 child agent를 만들지 않으며 completion counter도 수정하지 않는다. Root가 finding을 검토하고 필요한 state 또는 memory 변경을 적용한 뒤 다음을 실행한다.

```bash
./scripts/continuity review-complete
```

Review 주기는 비용 조절을 위한 기본값일 뿐이다. GOAL 변경 가능성, memory conflict, 반복 실패, 근거 없는 복잡성 증가가 보이면 일찍 실행한다.

## 12. Turn flow와 session 복구

```text
UserPromptSubmit hook: 누락된 Stop 복구 + due context 주입
  -> Root AGENTS 적용
  -> GOAL + CURRENT + INDEX 읽기
  -> 관련 active state + memory + evidence 읽기
  -> 최소 coherent work 수행
  -> CURRENT/active snapshot 갱신
  -> due이면 memory Skill 실행
  -> 더 긴 due이면 fresh reviewer 보고 회수
  -> Root가 수정과 결론 통합
  -> 최종 응답
  -> Stop hook: state hash가 달라진 turn이면 counter +1, {"continue": true}

SessionStart: 최초 시작/resume의 due 확인 + 누락된 Stop 복구
SessionEnd: thread 종료 시 최종 reconciliation 보조
```

이는 role을 자동 순환시키는 상태기계가 아니다. Ordinary work는 ordinary work로 남고, script는 유지보수가 필요한 시점을 알리는 역할만 한다.

## 13. Archive 경계

이전의 Level 2 architecture extension은 `codex-repository-framework/archive/`에 frozen, non-operational 상태로 보존한다. 현재 프레임은 다음을 하지 않는다.

- archive overlay를 대상 프로젝트에 복사하거나 병합
- archived Coder, Steward, Architecture Reviewer 호출
- archive 문서를 일반 작업 context로 load
- 구조 문제가 생겼다는 이유로 Level 2를 자동 활성화

구조 관련 문제도 먼저 현재 Root가 코드와 범용 memory 안에서 직접 다룬다. 별도 구조 체계가 정말 필요하면 사용자가 새 설계를 명시적으로 결정해야 한다. Archive는 과거 판단을 검토하라는 요청이 있을 때만 참고 자료로 연다.

## 14. 적용과 운영

새 프로젝트와 기존 프로젝트에 동일한 safe installer를 사용한다.

```bash
/path/to/codex-repository-framework/install-continuity /path/to/target-project --dry-run
/path/to/codex-repository-framework/install-continuity /path/to/target-project
```

Installer는 기존 root instruction의 managed block과 기존 hook JSON만 구조적으로 병합한다. 다른 기존 파일은 덮어쓰지 않는다. Root `AGENTS.override.md`가 활성 상태이면 auto mode가 중단되므로 override의 임시성 여부를 먼저 결정한다.

설치 직후 새 Codex 세션에서 다음을 한 번 실행한다.

```text
$initialize-project-continuity
```

Skill이 목표 결정을 충분히 확보하고 초기 문서를 검증한 뒤 `Continuity baseline`을 established로 바꾼다.

첫 작업 생성:

```bash
cp state/active/_template.md state/active/<task>.md
./scripts/continuity validate
./scripts/continuity status
```

Hook은 명령 실행 권한을 가지므로 프로젝트가 `.codex/hooks.json` 사용을 요청할 때 내용을 검토하고 신뢰한다. Team repository에서는 hook과 script 변경도 code review 대상으로 둔다.

`archive/`는 설치 대상에서 제외한다.

## 15. 공식 Codex 구조와의 대응

이 프레임은 별도의 proprietary loader를 만들지 않고 Codex가 제공하는 repository 구조를 사용한다.

- Root와 하위 지침: [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- Repository skill: [`.agents/skills`](https://learn.chatgpt.com/docs/build-skills)
- Custom reviewer role: [subagent configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- 저비용 turn/session trigger: [`.codex/hooks.json`](https://learn.chatgpt.com/docs/hooks)

활성 custom agent는 drift reviewer 하나이며 상세 역할은 전용 `.toml`에 둔다. Root `AGENTS.md`에는 호출 조건과 통합 책임만 둔다. Hook command는 repository 권한으로 실행되므로 설치 시 검토와 신뢰가 필요하다.

## 16. 핵심 판단

이 설계에서 값비싼 LLM은 의미 판단이 필요한 세 곳에만 사용된다.

- 프로젝트 도입 시 한 번 수행하는 continuity initialization
- 후보를 압축하고 충돌을 다루는 memory maintenance
- 기존 작업 관성에서 분리된 independent drift review

횟수 계산, due 판정, index 생성, schema validation은 단순 코드가 담당한다. 그 결과 자동화 비용을 낮추면서도 memory를 단순 append-only note보다 신뢰할 수 있게 유지한다.

프레임의 목표는 정보를 많이 쌓는 것이 아니다. 다음 세션이 얕은 경로로 올바른 목표와 판단 지점에 도달하고, 오래된 지식은 정기적으로 검증되며, 별도의 agent hierarchy 없이 메인 Codex가 작업을 계속하는 것이다.
