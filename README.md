# Codex Repository Continuity Framework

긴 작업을 여러 세션으로 나눠도 Codex가 장기 목표, 현재 상태, 이미 배운 제약을 잊지 않고 이어가게 하는 재사용 프레임입니다. 연구·백테스트뿐 아니라 구현, 운영, 문서화, 마이그레이션 등 장기 프로젝트 전반을 대상으로 합니다.

운영 프레임은 **Level 1 — Continuity 하나뿐**입니다. 상태가 변경된 Codex 턴은 모델 호출 없이 로컬 스크립트가 세고, 짧은 주기로 메모리 정리를 알리며, 더 긴 주기로 깨끗한 컨텍스트의 독립 drift review를 요청합니다. 이전 Level 2 architecture 설계는 비활성 archive로 봉인했습니다.

## 빠른 적용

새 프로젝트와 기존 프로젝트 모두 non-destructive installer를 사용합니다. 기존 root `AGENTS.md`에는 marker로 구분된 continuity block만 병합하고, 다른 내용은 보존합니다.

```bash
./codex-repository-framework/install-continuity /path/to/target-project --dry-run
./codex-repository-framework/install-continuity /path/to/target-project
```

Installer는 기존 파일을 덮어쓰지 않고 `AGENTS.md`의 managed block과 hooks만 구조적으로 병합합니다. 기본 32 KiB instruction budget을 넘는 프로젝트는 쓰기 전에 중단합니다. 적용 직후 Codex에서 `$initialize-project-continuity`를 한 번 실행해 프로젝트 근거와 사용자 결정으로 `GOAL`, `CURRENT`, 첫 active state의 기준을 잡습니다.

Hook은 Linux/macOS와 Windows 명령을 함께 설치합니다. Codex가 운영체제에 맞는 명령을 자동 선택하고, launcher가 Git root와 사용 가능한 Python 3.10+를 찾으므로 프로젝트 절대경로나 분석용 가상환경을 설정할 필요가 없습니다.

적용과 운영 방법은 [프레임워크 README](./codex-repository-framework/README.md), 현재 설계는 [v3.1 가이드](./docs/codex_repository_continuity_framework_guide_v3-1.md)를 참고하세요. [DOCX](./codex_repository_continuity_framework_guide_v3-1.docx)도 함께 제공합니다.

v2.x, v3.0, `codex-repository-framework/archive/`는 설계가 발전한 과정을 보존하는 이전 기록이며 현재 프레임의 설치·실행 대상이 아닙니다.
