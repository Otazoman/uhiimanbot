<div id = content>
<style type="text/css">
    th, td {
              width: 100px ;
    }
    thead, tbody {
      display: block;
    }
    tbody {
      overflow-x: hidden;
      overflow-y: scroll;
      height: 600px;
    }
</style>
<table border=1>
      <thead>
          <tr>
              <th>トレンドワード</th>
              <th>リンクURL</th>
              <th>検索ボリューム</th>
              <th>登録日</th>
          </tr>
      </thead>
      <tbody>
          {% for item in items %}
          <tr>
              <td>{{ item.title }}</td>
              <td>
                 <a href='{{ item.link }}' target="_blank" rel="noopener">
                  {{ item.link }} 
                 </a>
              </td>
              <td>{{ item.volume }}</td>
              <td>{{ item.published }}</td>
              </tr>
          {% endfor %}
      </tbody>
</table>
</div>
