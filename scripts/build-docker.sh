#!/bin/bash
# Docker 構建腳本 - 用於生成 pre-built images

set -e

# 顏色輸出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🐳 開始 Docker Image 構建...${NC}"

# 設定 image 版本（可從環境變數或預設值）
VERSION=${1:-latest}
REGISTRY=${2:-""}  # 例如：docker.io/yourusername

# 構建 backend image
echo -e "\n${YELLOW}構建 Backend Image...${NC}"
docker build \
  -t training-pm-ai-flow:backend-${VERSION} \
  -f ./backend/Dockerfile \
  ./backend

if [ -n "$REGISTRY" ]; then
  docker tag training-pm-ai-flow:backend-${VERSION} ${REGISTRY}/training-pm-ai-flow:backend-${VERSION}
  echo -e "${GREEN}✓ Backend tagged: ${REGISTRY}/training-pm-ai-flow:backend-${VERSION}${NC}"
else
  echo -e "${GREEN}✓ Backend 構建完成: training-pm-ai-flow:backend-${VERSION}${NC}"
fi

# 構建 frontend image
echo -e "\n${YELLOW}構建 Frontend Image...${NC}"
docker build \
  -t training-pm-ai-flow:frontend-${VERSION} \
  -f ./frontend/Dockerfile \
  ./frontend

if [ -n "$REGISTRY" ]; then
  docker tag training-pm-ai-flow:frontend-${VERSION} ${REGISTRY}/training-pm-ai-flow:frontend-${VERSION}
  echo -e "${GREEN}✓ Frontend tagged: ${REGISTRY}/training-pm-ai-flow:frontend-${VERSION}${NC}"
else
  echo -e "${GREEN}✓ Frontend 構建完成: training-pm-ai-flow:frontend-${VERSION}${NC}"
fi

echo -e "\n${GREEN}✅ 所有 Images 構建完成！${NC}"
echo -e "\n${YELLOW}使用方式：${NC}"
echo "1. 本地執行："
echo "   docker-compose -f docker-compose.prod.yml up"
echo ""
if [ -n "$REGISTRY" ]; then
  echo "2. 推送到 Registry："
  echo "   docker push ${REGISTRY}/training-pm-ai-flow:backend-${VERSION}"
  echo "   docker push ${REGISTRY}/training-pm-ai-flow:frontend-${VERSION}"
fi
