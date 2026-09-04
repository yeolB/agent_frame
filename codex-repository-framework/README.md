# Codex Repository Continuity Framework

이 번들은 긴 작업을 여러 Codex 세션으로 나눠도 목표, 현재 판단 지점, 검증 근거, 이미 배운 제약이 끊기지 않게 합니다. 특정 연구 절차를 강제하지 않고 어떤 프로젝트에도 같은 정보 구조를 사용합니다.

기본값은 Level 1입니다. 구조 문제가 실제로 반복될 때만 Level 2를 추가합니다.

## Level 1 — Continuity

대상 프로젝트 루트에 `level-1-continuity/`의 **내용**을 복사합니다.

```bash
cp -R /path/to/codex-repository-framework/level-1-continuity/. /path/to/target-project/
cd /path/to/target-project
chmod +x scripts/continuity
```

설치되는 구조는 다음과 같습니다.

```text
AGENTS.md                         # 시작 순서와 공통 운영 원칙
GOAL.md                           # 사용자가 소유하는 장기 기준
state/
├── CURRENT.md                    # 현재 작업을 가리키는 짧은 시작점
├── cadence.json                  # 비-LLM 주기 상태와 설정
└── active/<task>.md              # 세션 간 현재 작업 snapshot
memory/
├── INDEX.md                      # 자동 생성되는 조건부 memory router
└── records/MEM-*.md              # 근거·범위·효과가 있는 durable memory
.agents/skills/
└── maintain-project-memory/      # 메모리 선별·정리 절차
.codex/
├── hooks.json                    # 시작/종료 때 로컬 스크립트 실행
└── agents/drift-reviewer.toml    # 독립 read-only 장기 검토자
scripts/continuity                # 카운터, index, validation
```

### 처음 설정

1. 사용자가 `GOAL.md`에 실제 목적, 성공 기준, guardrail, 금지할 shortcut, 중단 조건, 현재 방향, 고정 가정을 적습니다.
2. 첫 active state를 만듭니다.

```bash
cp state/active/_template.md state/active/first-task.md
```

3. `state/CURRENT.md`의 `Primary task`와 `Active state`를 갱신합니다.
4. 상태를 확인합니다.

```bash
./scripts/continuity validate
./scripts/continuity status
```

Codex가 project hook 사용을 요청하면 파일 내용을 검토한 뒤 신뢰해야 합니다. Hook은 로컬 Python 스크립트만 실행하며 모델을 호출하지 않습니다.

## 세션에서 읽는 순서

```text
AGENTS.md
  -> GOAL.md
  -> state/CURRENT.md
  -> memory/INDEX.md
  -> CURRENT가 가리키는 active state
  -> 현재 조건과 맞는 memory record
  -> 필요한 코드와 근거
```

`CURRENT.md`는 한 개의 얕은 시작점입니다. 모든 상태를 복제하지 않고 primary task와 다음 행동을 가리킵니다. `state/active`는 작업별 현재 snapshot이며 명령 일지가 아닙니다.

## 범용 메모리

진행 중 발견은 먼저 active state의 `Memory Candidates`에 둡니다. 정리 시점에 `$maintain-project-memory`가 다음 기준으로 선별합니다.

- 미래의 의사결정이나 행동을 바꾼다.
- 비싼 재조사나 실패 반복을 막는다.
- 근거, 적용 범위, 불확실성, 재검토 조건을 명시할 수 있다.

레코드 유형은 `decision`, `lesson`, `failure`, `constraint`, `assumption`, `finding`입니다. 연구 결과도 이 형식에 들어가고, 코드 구조 판단이나 운영 제약도 별도 계층 없이 같은 형식에 들어갑니다. `memory/INDEX.md`의 trigger와 scope로 필요한 레코드만 읽습니다.

## 비-LLM 주기 관리

기본값은 다음과 같습니다.

- current/active state가 실제로 달라진 세션 3회마다 memory maintenance
- memory maintenance 5회마다 independent drift review

`SessionEnd` hook은 상태 파일의 hash가 이전과 달라졌는지만 계산합니다. `SessionStart` hook은 due 여부가 있을 때 짧은 안내 문장만 context에 추가합니다. 요약, 판단, 리뷰에는 모델을 쓰지만 **세기와 알림에는 모델을 쓰지 않습니다**.

주기는 `state/cadence.json`의 두 설정으로 바꿀 수 있습니다.

```json
{
  "memory_every_changed_sessions": 3,
  "review_every_memory_runs": 5
}
```

수동 명령은 다음과 같습니다.

```bash
./scripts/continuity status
./scripts/continuity next-id
./scripts/continuity index
./scripts/continuity validate
./scripts/continuity memory-complete
./scripts/continuity review-complete
```

단순 카운터가 agent의 행동을 자동 전환하거나 코드를 수정하지 않습니다. Due 신호가 생기면 root agent가 메모리 스킬을 호출하거나 reviewer를 한 번 생성하고, 결과를 통합한 뒤 completion 명령으로 카운터를 닫습니다.

## 독립 drift review

더 긴 주기에는 구현 세션의 관성을 줄이기 위해 fresh `drift_reviewer`를 별도 thread로 실행합니다. 가능한 한 대화 이력을 적게 상속하고 다음 원자료를 전달합니다.

- 원래 요청과 `GOAL.md`
- `state/CURRENT.md`와 관련 active state
- `memory/INDEX.md`와 관련 records
- 판단을 검증할 primary code, 결과, 로그

Reviewer는 read-only이며 수정이나 추가 agent 생성을 하지 않습니다. 목표 대체, 실패 반복, 근거 없는 범위 확장, 낡거나 충돌하는 memory를 찾아 root에 보고합니다. Root가 제안을 판단하고 필요한 수정을 적용한 뒤 `review-complete`를 실행합니다.

목표 변경이 필요해 보이거나 memory 충돌, 반복 실패, 근거 없는 복잡성 증가가 나타나면 카운터와 무관하게 일찍 검토할 수 있습니다.

## Level 2 — Architecture

다음 문제가 반복될 때만 [Level 2](./level-2-architecture/)를 검토합니다.

- 동작을 계속 잘못된 module이나 layer에 구현한다.
- ownership 또는 public boundary를 반복해서 재조사한다.
- dependency direction이나 local operational constraint가 반복해서 깨진다.
- 복잡한 subtree에서 필요한 코드와 지침을 지속적으로 찾지 못한다.

Level 2는 `ARCHITECTURE.md`, Steward, architecture-aware Coder/Reviewer, 필요한 위치의 local `AGENTS.md`를 선택적으로 추가합니다. 구조 지식도 Level 1 memory record를 사용하므로 두 번째 memory 체계를 만들지 않습니다.
