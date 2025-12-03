# MCP 기반 사실 확인 챗봇 에이전트

## 프로젝트 개요

MCP(Model Context Protocol)를 활용하여 다양한 주제에 대해 **사실 기반** 대화를 제공하는 독립형 챗봇 에이전트입니다.

## 핵심 기능

1. **사실 기반 대화**: 웹 검색, 위키피디아 등 외부 소스를 통해 검증된 정보 제공
2. **Multi-turn 대화**: 대화 컨텍스트를 유지하며 연속적인 대화 지원
3. **REST API**: 독립적으로 작동하는 Chat API 제공
4. **MCP 통합**: 다양한 MCP 서버와 연동하여 정보 수집

## 기술 스택

- **언어**: Python 3.11+
- **웹 프레임워크**: FastAPI (비동기 지원, 자동 문서화)
- **MCP 클라이언트**: mcp 라이브러리
- **LLM**: Claude API (anthropic 라이브러리)
- **세션 관리**: 인메모리 또는 Redis

## 프로젝트 구조

```
mcp_for_chat/
├── CLAUDE.md              # 프로젝트 문서
├── README.md              # 사용 가이드
├── requirements.txt       # 의존성
├── .env.example           # 환경변수 템플릿
├── src/
│   ├── __init__.py
│   ├── main.py            # FastAPI 앱 진입점
│   ├── config.py          # 설정 관리
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py      # API 라우트 정의
│   │   └── models.py      # Pydantic 모델
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── chatbot.py     # 챗봇 에이전트 핵심 로직
│   │   └── session.py     # 세션/컨텍스트 관리
│   └── mcp/
│       ├── __init__.py
│       ├── client.py      # MCP 클라이언트 래퍼
│       └── tools.py       # MCP 도구 정의
└── tests/
    ├── __init__.py
    ├── test_api.py
    └── test_agent.py
```

## API 설계

### 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| POST | `/chat` | 메시지 전송 및 응답 받기 |
| POST | `/chat/stream` | 스트리밍 응답 |
| GET | `/sessions/{session_id}` | 세션 정보 조회 |
| DELETE | `/sessions/{session_id}` | 세션 삭제 |
| GET | `/health` | 헬스체크 |

### 요청/응답 모델

```python
# 요청
{
    "session_id": "optional-uuid",  # 없으면 새 세션 생성
    "message": "오늘 날씨 어때?",
    "options": {
        "use_web_search": true,
        "language": "ko"
    }
}

# 응답
{
    "session_id": "uuid",
    "response": "현재 서울 날씨는...",
    "sources": ["https://..."],  # 참조한 소스
    "metadata": {
        "tools_used": ["web_search"],
        "tokens_used": 150
    }
}
```

## MCP 서버 연동 계획

사실 기반 대화를 위해 다음 MCP 서버들을 연동:

1. **Brave Search MCP**: 웹 검색을 통한 최신 정보 수집
2. **Fetch MCP**: 웹페이지 내용 가져오기
3. **(선택) Wikipedia MCP**: 백과사전 정보

## 구현 단계

### Phase 1: 기본 구조 (MVP)
- [ ] 프로젝트 초기 설정 (requirements.txt, .env)
- [ ] FastAPI 기본 구조 생성
- [ ] 간단한 챗봇 에이전트 (MCP 없이 Claude만 사용)
- [ ] 세션 관리 구현 (인메모리)
- [ ] 기본 API 엔드포인트

### Phase 2: MCP 통합
- [ ] MCP 클라이언트 설정
- [ ] Brave Search MCP 연동
- [ ] 도구 호출 로직 구현
- [ ] 사실 검증 프롬프트 최적화

### Phase 3: 고도화
- [ ] 스트리밍 응답 지원
- [ ] 소스 인용 기능
- [ ] 에러 처리 강화
- [ ] 테스트 코드 작성

## 개발 명령어

```bash
# 의존성 설치
pip install -r requirements.txt

# 개발 서버 실행
uvicorn src.main:app --reload --port 8000

# 테스트 실행
pytest tests/

# API 문서 확인
# http://localhost:8000/docs
```

## 환경 변수

```
ANTHROPIC_API_KEY=your-api-key
BRAVE_API_KEY=your-brave-api-key  # 웹 검색용
LOG_LEVEL=INFO
SESSION_TIMEOUT=3600  # 1시간
```

## 주요 고려사항

1. **사실 정확성**: 웹 검색 결과를 기반으로 답변하되, 불확실한 정보는 명시
2. **대화 컨텍스트**: 이전 대화 내용을 참조하여 자연스러운 대화 흐름 유지
3. **응답 시간**: MCP 도구 호출 시 지연 최소화
4. **비용 관리**: 불필요한 API 호출 줄이기
