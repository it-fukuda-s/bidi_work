#!/bin/bash
# Docker操作スクリプト for bidi-app

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_NAME="bidi-app"
CONTAINER_NAME="bidi-container"
PORT=8080

cd "$SCRIPT_DIR"

case "$1" in
    build)
        echo "🔨 Building Docker image..."
        docker build -t "$APP_NAME" .
        echo "✅ Build complete"
        ;;

    start)
        echo "🚀 Starting container with volume mount..."
        # 既存コンテナがあれば削除
        docker rm -f "$CONTAINER_NAME" 2>/dev/null || true
        # ボリュームマウント付きで起動
        docker run -d \
            -p "$PORT:$PORT" \
            --env-file app/.env \
            -v "$(pwd)/app/data:/workspace/app/data" \
            --name "$CONTAINER_NAME" \
            "$APP_NAME"
        echo "✅ Started at http://localhost:$PORT"
        echo "📁 Session DB: app/data/sessions.db (mounted)"
        ;;

    stop)
        echo "🛑 Stopping container..."
        docker stop "$CONTAINER_NAME" 2>/dev/null || true
        docker rm "$CONTAINER_NAME" 2>/dev/null || true
        echo "✅ Stopped"
        ;;

    restart)
        $0 stop
        $0 start
        ;;

    logs)
        echo "📋 Container logs:"
        docker logs "$CONTAINER_NAME" --tail 50 -f
        ;;

    status)
        echo "📊 Container status:"
        docker ps -a --filter "name=$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        ;;

    rebuild)
        echo "🔄 Rebuilding and restarting..."
        $0 build
        $0 start
        ;;

    *)
        echo "Usage: $0 {build|start|stop|restart|logs|status|rebuild}"
        echo ""
        echo "Commands:"
        echo "  build    - Build Docker image"
        echo "  start    - Start container with session DB volume mount"
        echo "  stop     - Stop and remove container"
        echo "  restart  - Stop and start container"
        echo "  logs     - Show container logs (follow mode)"
        echo "  status   - Show container status"
        echo "  rebuild  - Build and start (full redeploy)"
        exit 1
        ;;
esac
