# Level 2 — Architecture Extension

Level 1을 먼저 사용합니다. 다음과 같은 실패가 반복적으로 관측될 때만 이 확장을 설치합니다.

- behavior가 계속 잘못된 module이나 layer에 놓인다.
- ownership과 public boundary를 매번 다시 조사한다.
- dependency cycle이나 내부 model 누출이 반복된다.
- 큰 subtree에서 필요한 context와 local command를 계속 찾지 못한다.

성장한 코드베이스 자체는 설치 이유가 아닙니다. 실제 반복 비용이나 오류를 active state 또는 experiment ledger에서 확인할 수 있어야 합니다.

## 설치

1. `overlay/`의 내용을 대상 프로젝트 루트에 복사합니다.
2. `AGENTS.additions.md`에서 현재 문제에 필요한 절만 루트 `AGENTS.md`에 병합합니다.
3. `ARCHITECTURE.md`에는 이상적인 목표가 아니라 현재 구조를 기록합니다.
4. ownership 혼동이 실제로 발생한 domain만 `memory/domains/_template.md`로 만듭니다.
5. 하위 `AGENTS.md`와 local `ARCHITECTURE.md`는 해당 subtree의 반복 문제가 있을 때만 추가합니다.

```bash
cp -R /path/to/level-2-architecture/overlay/. /path/to/target-project/
```

기존 `ARCHITECTURE.md`, `.codex/`, `memory/`, `templates/`가 있다면 덮어쓰지 말고 병합합니다.

## 실행 모델

이 확장은 daemon이나 자동 순환 시스템을 만들지 않습니다. 메인 세션은 필요한 시점에 역할을 별도 작업으로 생성하고 결과를 통합합니다.

```text
구조 문제 조사: Root -> Steward -> Root decision
구현:          Root -> Coder -> Architecture Reviewer -> Root integration
```

동일 파일을 수정하는 역할은 순차 실행합니다. Drift review는 Level 1의 목표 검토이고, Architecture Reviewer는 구현 위치와 경계를 검토하므로 목적이 다릅니다.
