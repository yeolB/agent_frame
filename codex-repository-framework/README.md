# Codex Repository Continuity Framework

이 번들은 긴 작업을 여러 Codex 세션으로 나눠도 목표, 현재 판단 지점, 검증 근거, 이미 배운 제약이 끊기지 않게 합니다. 또한 큰 작업을 시작할 때 현재 해법에 갇히지 않았는지 짧게 점검하고, 장기 reviewer가 전략과 누적 구조를 함께 살핍니다. 특정 연구 절차를 강제하지 않고 어떤 프로젝트에도 같은 정보 구조를 사용합니다.

운영 가능한 프레임은 Level 1 하나입니다. 이전 architecture extension은 `archive/`에 보존하지만 설치하거나 agent context로 사용하지 않습니다.

## Level 1 — Continuity

새 프로젝트와 기존 프로젝트 모두 installer로 적용합니다. 대상 경로는 먼저 초기화된 Git repository의 root여야 하며 Python 3.10+가 필요합니다.

```bash
/path/to/codex-repository-framework/install-continuity /path/to/target-project --dry-run
/path/to/codex-repository-framework/install-continuity /path/to/target-project
```

Installer의 동작은 다음과 같습니다.

- 대상이 Git root인지와 현재 운영체제에서 사용할 수 있는 Python 3.10+ hook runtime을 먼저 검사합니다.
- Root instruction이 없으면 canonical `AGENTS.md`를 만듭니다.
- 기존 `AGENTS.md`가 있으면 `BEGIN/END CODEX CONTINUITY` marker 사이의 작은 block만 추가하거나 갱신합니다.
- 기존 `.codex/hooks.json`은 다른 hook을 보존하면서 continuity hook만 병합합니다.
- AF 소유 파일(공통 Skill 3개와 설정, drift reviewer, runtime/launcher, active·memory의 `_template.md`)은 명시적 관리 목록에 따라 교체합니다. 프로젝트별 절차는 별도 이름의 Skill에 작성합니다.
- 프로젝트 소유 `GOAL.md`, `CURRENT.md`, cadence, memory index·records, active 작업 및 별도 Skill은 보존합니다. 없는 초기 파일만 생성합니다.
- 모든 쓰기가 성공한 뒤 `state/af-install.json`에 소스 Git 리비전, 수정 여부, 설치 시각, 관리 파일·구간 목록을 기록합니다.
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
├── maintain-project-memory/       # 메모리 선별·정리 절차
└── plan-substantial-work/         # 큰 구현 전 task-scoped 전략 점검
.codex/
├── hooks.json                    # 턴 전후와 세션 복구 때 로컬 스크립트 실행
└── agents/drift-reviewer.toml    # 독립 read-only 장기 검토자
scripts/
├── continuity                    # 카운터, index, validation
├── continuity-posix              # Linux/macOS Python launcher
└── continuity-windows.ps1        # Windows Python launcher
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

Codex가 project hook 사용을 요청하면 파일 내용을 검토한 뒤 신뢰해야 합니다. Hook은 bundled OS launcher와 로컬 Python 스크립트만 실행하며 모델을 호출하지 않습니다.

### 운영체제별 자동 실행

`.codex/hooks.json`의 각 handler에는 POSIX용 `command`와 Windows 전용 `commandWindows`가 함께 들어갑니다. Codex가 운영체제에 맞는 필드를 자동 선택합니다.

- Linux/macOS: Git root에서 `scripts/continuity-posix`를 찾고 `python3`, `python` 순서로 Python 3.10+를 선택합니다.
- Windows: PowerShell이 Git root에서 `scripts/continuity-windows.ps1`을 찾고 `py -3`, `python`, `python3` 순서로 실제 실행 가능한 Python 3.10+를 선택합니다.
- 둘 다 project absolute path나 project virtual environment를 저장하지 않습니다.

Windows PowerShell에서도 같은 installer를 사용합니다.

```powershell
py -3 .\codex-repository-framework\install-continuity C:\path\to\target-project --dry-run
py -3 .\codex-repository-framework\install-continuity C:\path\to\target-project
```

Git, PowerShell 또는 호환 Python이 없으면 installer가 쓰기 전에 중단합니다. 업데이트도 최초 설치와 같은 명령을 사용합니다. AF 소유 파일은 자동 교체하며 `--replace-runtime`은 기존 호출 호환용으로만 남아 있습니다.

PTY는 `state/af-install.json`의 `revision`을 최신 AF 소스 Git HEAD와 비교하면 됩니다. 같고 `source_dirty`가 `false`이면 해당 소스 리비전으로 설치된 상태입니다. 리비전이 다르면 업데이트 후보이며, 기록이 없거나 revision이 null이거나 dirty가 true/null이면 확인되지 않은 설치로 취급합니다. 이 기록은 로컬 AF 파일의 사후 변경까지 감시하는 무결성 검사는 아닙니다. Git metadata 없는 배포도 설치되지만 리비전은 null입니다. Installer 자체는 네트워크 조회나 주기 업데이트를 수행하지 않습니다.

`--dry-run`은 기록도 쓰지 않습니다. 동일 설치의 재실행은 설치 시각을 바꾸지 않습니다. 실패 시 새 리비전을 기록하지 않으며, 파일별 쓰기이므로 중간 실패는 일부 파일만 갱신된 상태일 수 있습니다. 같은 설치 명령을 다시 실행해 완료합니다. 관리 목록에서 사라진 파일을 자동 삭제하지는 않습니다.

Hook 정의가 새로 설치되거나 바뀌면 `/hooks`에서 내용을 검토하고 다시 신뢰해야 합니다.

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

## 큰 작업 전 Planner

큰 기능, 여러 module·interface를 건드리는 변경, 중요한 refactor·migration, 방향이 불명확한 구현, 새 dependency·service 도입처럼 잘못된 방향의 재작업 비용이 큰 경우에는 main Codex가 `$plan-substantial-work`를 먼저 사용합니다. 작은 local bug fix나 기계적 변경에는 사용하지 않습니다. 파일 수나 예상 line 수 같은 고정 threshold 대신 **잘못된 접근을 택했을 때 의미 있는 재작업이 생기는가**로 판단합니다.

Planner는 전체 repository architecture를 정기 감사하지 않습니다. 현재 task에 필요한 `GOAL`, current/active state, 관련 memory, 관련 code·interface·evidence만 읽고 다음을 확인합니다.

- 실제 outcome과 근본 bottleneck이 무엇인지
- 현재 구현이 원인 대신 증상만 다루는지
- 제거·단순화·기존 capability 재사용으로 incremental work를 없앨 수 있는지
- sunk cost가 없다면 같은 접근을 다시 선택할지
- 대안의 leverage가 전환 비용과 risk를 실제로 넘는지

기존 방향 유지도 정상 결론입니다. 결과는 별도 `PLAN.md`가 아니라 primary active state의 `Decisions and Rationale` 아래 짧은 `Strategy Checkpoint`와 갱신된 `Next Action`으로만 남깁니다. 그 뒤 같은 root agent가 ordinary execution을 계속하며 새 agent, hook, counter, 실행 mode를 만들지 않습니다.

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

Reviewer는 read-only이며 수정이나 추가 agent 생성을 하지 않습니다. 기존 continuity 점검에 다음 두 관점을 더합니다.

- **전략:** 실제 진전이 있어도 낮은 leverage의 solution space에 갇혀 있는지, sunk-cost bias나 잘못 잡은 bottleneck 때문에 제거 가능한 일을 계속 최적화하는지 확인합니다.
- **누적 architecture:** 서로 무관한 module의 coupling, 깊거나 순환하는 dependency, god module, layer leakage, 큰 change blast radius, 책임 중복과 accidental abstraction이 쌓였는지 repository-wide로 확인합니다.

단순히 불완전하거나 문제 자체가 복잡해서 생긴 구조는 finding이 아닙니다. Reviewer는 먼저 top-level structure, manifests, 직전 review 이후 diff, 기존 구조 자료를 저비용으로 훑고 신호가 있을 때만 깊게 조사합니다. 이미 dependency/call graph, impact analysis, symbol 관계, cycle·fan metric 같은 도구나 산출물이 있으면 근거로 활용하지만 새 graph system을 설치하거나 hard dependency로 만들지 않습니다. 도구가 없으면 manifests, imports, symbols, tests와 targeted search로 대체합니다.

각 finding은 `goal`, `strategy`, `architecture`, `memory`로 구분하고 근거·영향·조치·확신도를 설명합니다. Architecture finding은 교정 범위와 전환 비용도 포함합니다. “현재 접근이 적절하므로 계속한다”도 정상 결론입니다. Root가 제안을 판단하고 필요한 수정을 적용한 뒤 `review-complete`를 실행합니다.

목표 변경이 필요해 보이거나 memory 충돌, 반복 실패, 근거 없는 복잡성 증가가 나타나면 카운터와 무관하게 일찍 검토할 수 있습니다.

## Archive 경계

[`archive/`](./archive/)는 이전의 architecture governance, Coder, Steward, Architecture Reviewer 설계를 기록으로만 보존합니다. 다음 원칙을 적용합니다.

- 대상 프로젝트에 복사하거나 병합하지 않습니다.
- Root가 archive의 agent를 호출하지 않습니다.
- 일반 작업 중 archive 문서를 context로 읽지 않습니다.
- 사용자가 과거 설계를 명시적으로 요청할 때만 참고합니다.

향후 구조 문제가 생기더라도 archive를 자동으로 활성화하지 않습니다. 현재 Level 1 reviewer가 구조를 진단하고 root가 필요한 코드 변경을 직접 수행합니다. 별도 구조 체계가 정말 필요하면 사용자가 새 설계를 결정합니다.
