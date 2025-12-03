# MCP Fact Chatbot

MCP(Model Context Protocol) 기반의 사실 확인 챗봇 API 서버입니다.

## 특징

- **사실 기반 응답**: 웹 검색을 통해 실시간 정보 제공
- **Multi-turn 대화**: 세션 기반 대화 컨텍스트 유지
- **REST API**: 간단한 HTTP API로 통합 가능
- **소스 인용**: 응답에 참조 URL 포함

## 빠른 시작

### 1. 설치

```bash
# 저장소 클론
git clone <repository-url>
cd mcp_for_chat

# 의존성 설치
pip install -r requirements.txt

# uv 설치 (MCP 서버 실행에 필요)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 환경 설정

```bash
cp .env.example .env
# .env 파일에 ANTHROPIC_API_KEY 설정
```

### 3. 서버 실행

```bash
uvicorn src.main:app --reload --port 8000
```

### 4. API 사용

```bash
# 새 대화 시작
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "오늘 테슬라 주가 어때?"}'

# 응답 예시
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "현재 테슬라(TSLA) 주가는...",
  "sources": ["https://..."]
}

# 대화 이어가기 (session_id 사용)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "550e8400-e29b-41d4-a716-446655440000", "message": "작년 대비 어때?"}'
```

## API 엔드포인트

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/chat` | 메시지 전송 및 응답 받기 |
| GET | `/sessions/{session_id}` | 세션 정보 조회 |
| DELETE | `/sessions/{session_id}` | 세션 삭제 |
| GET | `/health` | 서버 상태 확인 |

## 환경 변수

| 변수 | 필수 | 기본값 | 설명 |
|------|------|--------|------|
| `ANTHROPIC_API_KEY` | O | - | Claude API 키 |
| `SEARCH_PROVIDER` | X | `duckduckgo` | 검색 엔진 (`duckduckgo` 또는 `brave`) |
| `BRAVE_API_KEY` | △ | - | Brave Search 사용 시 필요 |
| `SESSION_TIMEOUT` | X | `3600` | 세션 만료 시간 (초) |
| `LOG_LEVEL` | X | `INFO` | 로그 레벨 |

## 검색 엔진 설정

### DuckDuckGo (기본값, 테스트용)
```bash
# API 키 불필요
SEARCH_PROVIDER=duckduckgo
```

### Brave Search (프로덕션)
```bash
SEARCH_PROVIDER=brave
BRAVE_API_KEY=your-brave-api-key
```

## API 문서

서버 실행 후 http://localhost:8000/docs 에서 Swagger UI로 API 문서 확인 가능

## 라이선스

MIT
