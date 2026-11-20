# Solar Huawei Dashboard

Tableau de bord personnel pour deux sites FusionSolar, déployable avec Docker Compose.

## Démarrage local

```powershell
Copy-Item .env.example .env
docker compose up --build
```

- Interface : http://localhost:8080
- API : http://localhost:8000/docs

Le collecteur reste volontairement en mode attente tant que les endpoints FusionSolar
et le format exact de l'authentification n'ont pas été confirmés. La clé API doit
uniquement être renseignée dans `.env` sur le serveur et ne doit jamais être commitée.

## Déploiement Ubuntu

Le même `docker-compose.yml` peut être utilisé sur le serveur. Le tunnel Cloudflare
devra pointer vers `http://frontend:80` sur le réseau Docker, avec une protection
Cloudflare Access ou une authentification applicative.
