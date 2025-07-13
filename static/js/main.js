async function loadArticles() {
  const res = await fetch('/articles?limit=10');
  const data = await res.json();
  const container = document.getElementById('articles');
  data.forEach(a => {
    const div = document.createElement('div');
    div.className = 'article';
    div.innerHTML = `
      <a href="${a.url}" target="_blank">${a.title}</a>
      <p>Категорія: ${a.category}, Тональність: ${a.sentiment}</p>
    `;
    container.appendChild(div);
  });
}

window.onload = loadArticles;
