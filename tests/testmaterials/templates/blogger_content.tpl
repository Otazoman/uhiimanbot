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
              <th>カテゴリー</th>
              <th>サイト名</th>
              <th>記事タイトル</th>
              <th>リンクURL</th>
              <th>頻出ワード・要約等</th>
              <th>登録日</th>
          </tr>
      </thead>
      <tbody>
          {% for item in items %}
          <tr>
              <td>{{ item.category }}</td>
              <td>{{ item.name }}</td>
              <td>{{ item.title }}</td>
              <td>
                 <a href='{{ item.link }}' target="_blank" rel="noopener">
                  {{ item.link }} 
                 </a>
              </td>
              <td>{{ item.summary }}</td>
              <td>{{ item.published }}</td>
              </tr>
          {% endfor %}
      </tbody>
</table>
</div>
