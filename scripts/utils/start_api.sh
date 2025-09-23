#!/bin/bash

# Script de gestion de l'API FastAPI
API_NAME="cde_api"
DOCKER_SERVICE="api"
API_BASE="http://localhost:8000"

# Fonction d'affichage
print_status() {
    echo "🤖 $1"
}

# -------------------------
# Vérification des arguments
# -------------------------
if [ $# -eq 0 ]; then
    echo "Usage: $0 [start|stop|restart|status|logs]"
    exit 1
fi

case "$1" in
    start)
        # -------------------------
        # DÉMARRAGE DE L'API
        # -------------------------
        print_status "Vérification de l'état actuel de l'API..."
        
        if [ "$(docker ps -q -f name=$API_NAME)" ]; then
            print_status "⚠️ Une instance de l'API est déjà en cours. Arrêt préalable..."
            docker stop $API_NAME > /dev/null 2>&1
            docker rm $API_NAME > /dev/null 2>&1
        fi

        print_status "🚀 Construction et lancement de l'API..."
        docker-compose build $DOCKER_SERVICE
        docker-compose up -d $DOCKER_SERVICE

        print_status "⌛ Attente que l'API soit disponible..."
        MAX_RETRIES=30
        RETRY_COUNT=0
        
        until curl -s "$API_BASE/health" >/dev/null; do
            sleep 2
            RETRY_COUNT=$((RETRY_COUNT+1))
            if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
                print_status "❌ Timeout: L'API ne répond pas après 60 secondes"
                print_status "📋 Vérifiez les logs avec: $0 logs"
                exit 1
            fi
        done
        
        print_status "✅ API est prête et accessible sur $API_BASE"
        print_status "📋 Pour voir les logs: $0 logs"
        print_status "🛑 Pour arrêter: $0 stop"
        ;;

    stop)
        # -------------------------
        # ARRÊT DE L'API
        # -------------------------
        print_status "Arrêt de l'API..."
        
        if [ "$(docker ps -q -f name=$API_NAME)" ]; then
            docker-compose stop $DOCKER_SERVICE
            print_status "✅ API arrêtée avec succès"
        else
            print_status "ℹ️ L'API n'est pas en cours d'exécution"
        fi
        ;;

    restart)
        # -------------------------
        # REDÉMARRAGE DE L'API
        # -------------------------
        print_status "Redémarrage de l'API..."
        $0 stop
        sleep 2
        $0 start
        ;;

    status)
        # -------------------------
        # ÉTAT DE L'API
        # -------------------------
        if [ "$(docker ps -q -f name=$API_NAME)" ]; then
            print_status "✅ API en cours d'exécution"
            echo "📊 URL: $API_BASE"
            echo "🐳 Container: $API_NAME"
        else
            print_status "❌ API arrêtée"
            # Vérifier si le container existe mais est arrêté
            if [ "$(docker ps -a -q -f name=$API_NAME)" ]; then
                echo "ℹ️ Container existant mais arrêté"
            fi
        fi
        ;;

    logs)
        # -------------------------
        # AFFICHAGE DES LOGS
        # -------------------------
        print_status "Affichage des logs de l'API..."
        docker-compose logs -f $DOCKER_SERVICE
        ;;

    down)
        # -------------------------
        # ARRÊT COMPLET (avec suppression)
        # -------------------------
        print_status "Arrêt et suppression du container..."
        docker-compose down $DOCKER_SERVICE
        ;;

    build)
        # -------------------------
        # RECONSTRUCTION SEULEMENT
        # -------------------------
        print_status "Reconstruction de l'image API..."
        docker-compose build $DOCKER_SERVICE
        print_status "✅ Construction terminée"
        ;;

    *)
        echo "Usage: $0 [start|stop|restart|status|logs|down|build]"
        echo ""
        echo "Commandes:"
        echo "  start   - Démarre l'API"
        echo "  stop    - Arrête l'API"
        echo "  restart - Redémarre l'API"
        echo "  status  - Affiche l'état de l'API"
        echo "  logs    - Affiche les logs en temps réel"
        echo "  down    - Arrête et supprime le container"
        echo "  build   - Reconstruit l'image sans démarrer"
        exit 1
        ;;
esac
