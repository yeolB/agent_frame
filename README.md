# Codex Repository Continuity Framework

긴 작업을 여러 세션으로 나눠도 Codex가 장기 목표, 현재 상태, 이미 배운 제약을 잊지 않고 이어가게 하는 재사용 프레임입니다. 연구·백테스트뿐 아니라 구현, 운영, 문서화, 마이그레이션 등 장기 프로젝트 전반을 대상으로 합니다.

운영 프레임은 **Level 1 — Continuity 하나뿐**입니다. 변경된 작업 세션은 모델 호출 없이 로컬 스크립트가 세고, 짧은 주기로 메모리 정리를 알리며, 더 긴 주기로 깨끗한 컨텍스트의 독립 drift review를 요청합니다. 이전 Level 2 architecture 설계는 비활성 archive로 봉인했습니다.

## 빠른 적용

새 프로젝트 또는 기존 프로젝트의 루트에 Level 1의 내용을 복사합니다.

```bash
cp -R /path/to/agent_frame/codex-repository-framework/level-1-continuity/. .
chmod +x scripts/continuity
```

복사 후 사용자가 `GOAL.md`를 작성하고 `state/active/_template.md`에서 첫 작업 상태를 만듭니다. Codex는 명시적인 사용자 요청 없이 `GOAL.md`를 변경하지 않습니다.

적용과 운영 방법은 [프레임워크 README](./codex-repository-framework/README.md), 현재 설계는 [v3.1 가이드](./docs/codex_repository_continuity_framework_guide_v3-1.md)를 참고하세요. [DOCX](./codex_repository_continuity_framework_guide_v3-1.docx)도 함께 제공합니다.

v2.x, v3.0, `codex-repository-framework/archive/`는 설계가 발전한 과정을 보존하는 이전 기록이며 현재 프레임의 설치·실행 대상이 아닙니다.
