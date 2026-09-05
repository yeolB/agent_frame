# Codex Repository Continuity Framework

이 번들은 긴 작업을 여러 Codex 세션으로 나눠도 목표, 현재 판단 지점, 검증 근거, 이미 배운 제약이 끊기지 않게 합니다. 특정 연구 절차를 강제하지 않고 어떤 프로젝트에도 같은 정보 구조를 사용합니다.

운영 가능한 프레임은 Level 1 하나입니다. 이전 architecture extension은 `archive/`에 보존하지만 설치하거나 agent context로 사용하지 않습니다.

## Level 1 — Continuity

새 프로젝트와 기존 프로젝트 모두 installer로 적용합니다.

```bash
/path/to/codex-repository-framework/install-continuity /path/to/target-project --dry-run
/path/to/codex-repository-framework/install-continuity /path/to/target-project
```

Installer의 동작은 다음과 같습니다.

- Root instruction이 없으면 canonical `AGENTS.md`를 만듭니다.
- 기존 `AGENTS.md`가 있으면 `BEGIN/END CODEX CONTINUITY` marker 사이의 작은 block만 추가하거나 갱신합니다.
- 기존 `.codex/hooks.json`은 다른 hook을 보존하면서 continuity hook만 병합합니다.
- 그 밖의 기존 파일은 덮어쓰지 않고 manual review 대상으로 출력합니다.
- 쓰기 전에 project instruction chain의 byte 크기를 검사합니다.

Root에 `AGENTS.override.md`가 있으면 같은 위치의 `AGENTS.md`를 가리므로 auto mode는 중단합니다. 임시 override를 제거하거나, 내용을 검토한 후 다음처럼 적용 대상을 명시합니다.

```bash
/path/to/codex-repository-framework/install-continuity /path/to/target-project \
  --instruction-file AGENTS.override.md
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
├── initialize-project-continuity/ # 명시적으로 한 번 실행하는 초기화
└── maintain-project-memory/       # 메모리 선별·정리 절차
.codex/
├── hooks.json                    # 턴 전후와 세션 복구 때 로컬 스크립트 실행
└── agents/drift-reviewer.toml    # 독립 read-only 장기 검토자
scripts/continuity                # 카운터, index, validation
```

### 처음 설정

설치 직후 새 Codex 세션에서 다음 Skill을 명시적으로 한 번 실행합니다.

```text
$initialize-project-continuity
```

이 Skill은 프로젝트의 README, manifests, entry points, test·CI 설정과 기존 지침을 조사하고, 사용자에게 부족한 목표 결정을 확인한 뒤 다음 기준선을 만듭니다.

- 사용자 소유의 `GOAL.md`
- primary task 하나를 가리키는 `state/CURRENT.md`
- 첫 `state/active/<task>.md`
- 근거가 있을 때만 생성하는 최소 memory records
- 기존 project rules를 보존한 compact root `AGENTS.md`

초기화가 끝나면 `CURRENT.md`의 `Continuity baseline`이 `established YYYY-MM-DD`가 됩니다. 이미 established 상태라면 Skill은 사용자가 `rebaseline`을 명시하지 않는 한 문서를 다시 쓰지 않습니다. Rebaseline에서도 `GOAL.md` 변경은 사용자 결정을 먼저 받으며 cadence와 기존 memory를 초기화하지 않습니다.

수동으로 첫 active state를 만들어야 할 때만 다음 template을 사용합니다.

```bash
cp state/active/_template.md state/active/first-task.md
```

상태를 확인합니다.

```bash
./scripts/continuity validate
./scripts/continuity status
```

Codex가 project hook 사용을 요청하면 파일 내용을 검토한 뒤 신뢰해야 합니다. Hook은 로컬 Python 스크립트만 실행하며 모델을 호출하지 않습니다.

## 기존 AGENTS.md가 큰 경우

Codex는 root부터 현재 작업 디렉터리까지 instruction을 합치며 기본 project instruction 한도는 32 KiB입니다. Installer는 가장 큰 project chain을 계산해 한도를 넘으면 쓰기 전에 중단하고, 75% 이상이면 경고합니다. Global instruction 크기는 이 계산에 포함되지 않으므로 여유를 두는 편이 좋습니다.

큰 `AGENTS.md`를 여러 자동 로드 파일로 단순 분할하지 않습니다. 같은 디렉터리에서는 `AGENTS.override.md` 또는 `AGENTS.md` 중 하나만 선택되기 때문입니다. 대신 다음처럼 줄입니다.

- Root에는 모든 작업에 항상 필요한 금지사항, 핵심 명령, context routing만 둡니다.
- 배포, migration, 특정 test workflow 같은 절차는 `.agents/skills/<name>/SKILL.md`로 옮깁니다.
- 현재 진행 상황은 `state/CURRENT.md`와 active state로 옮깁니다.
- 누적된 교훈과 예외는 trigger가 있는 memory record로 옮깁니다.
- 설명형 architecture와 긴 예시는 일반 문서에 두고 관련 Skill이나 memory에서 필요할 때만 연결합니다.
- formatting과 정적 규칙은 가능한 한 formatter, linter, test, CI가 검사하게 합니다.
- 특정 subtree에만 필요한 짧은 override는 그 subtree의 `AGENTS.md`에 둡니다. 이 지침이 필요하면 Codex를 해당 경로에서 시작합니다.

한도를 의도적으로 높인 프로젝트만 실제 `project_doc_max_bytes` 설정과 일치하도록 `--agent-limit`과 `--allow-over-budget`을 사용합니다.

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

- current/active state가 실제로 달라진 턴 3회마다 memory maintenance
- memory maintenance 5회마다 independent drift review

여기서 턴은 `사용자 프롬프트 1회 -> Codex 작업 -> 최종 응답 1회`입니다. `Stop` hook이 `CURRENT.md`와 active-state 파일의 hash 변화를 확인해 해당 턴을 셉니다. 성공 시 Codex가 정상적으로 멈추도록 `{"continue": true}`를 출력합니다. 다음 `UserPromptSubmit` hook은 due일 때만 짧은 안내를 context에 추가합니다.

`SessionStart`는 처음 열기와 resume 시 due 상태를 알리고, 이전 `Stop`이 실행되지 않은 비정상 종료의 hash 차이를 복구합니다. `SessionEnd`도 마지막 복구·정리를 위한 보조 hook일 뿐 정상 cadence의 필수 카운터가 아닙니다. 어느 경로가 먼저 복구해도 저장된 hash 때문에 같은 변경을 두 번 세지 않습니다. 요약, 판단, 리뷰에는 모델을 쓰지만 **세기와 알림에는 모델을 쓰지 않습니다**.

주기는 `state/cadence.json`의 두 설정으로 바꿀 수 있습니다.

```json
{
  "memory_every_changed_turns": 3,
  "review_every_memory_runs": 5
}
```

이전 v1 상태의 `memory_every_changed_sessions`와 `changed_sessions_since_memory`는 새 script가 처음 상태를 저장할 때 turn 기반 v2 키로 값을 보존해 옮깁니다.

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

## Archive 경계

[`archive/`](./archive/)는 이전의 architecture governance, Coder, Steward, Architecture Reviewer 설계를 기록으로만 보존합니다. 다음 원칙을 적용합니다.

- 대상 프로젝트에 복사하거나 병합하지 않습니다.
- Root가 archive의 agent를 호출하지 않습니다.
- 일반 작업 중 archive 문서를 context로 읽지 않습니다.
- 사용자가 과거 설계를 명시적으로 요청할 때만 참고합니다.

향후 구조 문제가 생기더라도 archive를 자동으로 활성화하지 않습니다. 현재 Level 1 안에서 문제를 다루고, 별도 구조가 정말 필요하면 사용자가 새 설계를 결정합니다.
