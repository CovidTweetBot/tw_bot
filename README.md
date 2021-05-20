# tw-bot

Robot que publica tweets con reportes gráficos sobre el comportamiento de algunos indicadores relacionados al Covid-19 en Perú 


## Requisitos

- El script asume que existen imágenes en la ruta `./images/sinadef/not_processed/<region_name>.png`. La ruta genérica para cualquier conjunto de datos sería `./images/<dataset>/nnot_processed/<region_name>.png`

## Ejemplos de uso

```
python tw_bot.py --twitter_consumer_key=<twitter_consumer_key> --twitter_consumer_secret=<twitter_consumer_secret> --twitter_access_token=<twitter_access_token> --twitter_access_token_secret=<twitter_access_token_secret>
```

o pasando los parámetros mediante variables de entorno
```
export TWITTER_CONSUMER_KEY=<twitter_consumer_key>
export TWITTER_CONSUMER_SECRET=<twitter_consumer_secret>
export TWITTER_ACCESS_TOKEN=<twitter_access_token>
export TWITTER_ACCESS_TOKEN_SECRET=<twitter_access_token_secret>
python tw_bot.py
```