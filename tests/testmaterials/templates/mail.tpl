◆トレンドワード                                                     
══════════════════════════════════════════════════════════════════════════════════
   検索ワード                        検索ボリューム    
------------------------------------------------------
{% for trend in trends %}
   {{ trend.title }}                {{ trend.volume }}
------------------------------------------------------
{% endfor %}


◆対象記事                                                  
══════════════════════════════════════════════════════════════════════════════════
   サイト名              記事タイトル          ヒットワード          リンク
----------------------------------------------------------------------------------
{% for item in items %}
   {{ item.name }}   {{ item.title }}  {{ item.hitwords}}   {{ item.link }}
----------------------------------------------------------------------------------
{% endfor %}
