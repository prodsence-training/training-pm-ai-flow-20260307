# Frontend Dockerfile
FROM node:18-alpine AS base

# 安裝依賴階段
FROM base AS deps
WORKDIR /app

COPY package*.json ./
RUN npm ci

# 建構階段
FROM base AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# 確保 public 目錄存在
RUN mkdir -p ./public

ENV NEXT_PUBLIC_API_URL=http://localhost:8000/api

RUN npm run build

# 生產階段
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production

# 複製建構輸出
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
