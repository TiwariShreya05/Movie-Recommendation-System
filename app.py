import streamlit as st
import pickle
import pandas as pd
import requests
import streamlit.components.v1 as components 


TMDB_API_KEY = "522a3b9f8596353a8a28fbb4dc6a5071"

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
        r = requests.get(url, timeout=6)
        r.raise_for_status()
        data = r.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except RequestException:
        pass
    return "https://via.placeholder.com/300x450?text=No+Image"

def fetch_details(movie_id):
    result = {"vote_average": 0.0, "youtube_key": None}
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
        r = requests.get(url, timeout=6)
        r.raise_for_status()
        data = r.json()
        result["vote_average"] = data.get("vote_average", 0.0)
    except RequestException:
        pass

    try:
        vurl = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}"
        vr = requests.get(vurl, timeout=6)
        vr.raise_for_status()
        vlist = vr.json().get("results", [])
        yt_candidates = [v for v in vlist if v.get("site") == "YouTube" and v.get("type") in ("Trailer","Teaser")]
        if yt_candidates:
            result["youtube_key"] = yt_candidates[0].get("key")
    except RequestException:
        pass

    return result

def recommend(movie_title):
    movie_index = movies[movies['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    top_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:9]

    out_titles = []
    out_posters = []
    out_star_strings = []
    out_embed_keys = []

    for idx, _score in top_list:
        mid = movies.iloc[idx].movie_id
        title_text = movies.iloc[idx].title

        poster_url = fetch_poster(mid)
        details = fetch_details(mid)
        vote_val = details.get("vote_average", 0.0)
        stars_count = int(round(vote_val / 2.0))
        star_string = "★" * stars_count + "☆" * (5 - stars_count)
        yt_key = details.get("youtube_key")

        out_titles.append(title_text)
        out_posters.append(poster_url)
        out_star_strings.append(star_string)
        out_embed_keys.append(yt_key)

    return out_titles, out_posters, out_star_strings, out_embed_keys

st.set_page_config(page_title="Movie Recommender", layout="wide")

# Load data
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

# Load CSS
try:
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

st.markdown("<h1 class='main-heading'>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([4,1])
with col1:
    movie_list = movies['title'].tolist()
    selected_movie = st.selectbox("Search or select a movie:", movie_list)
with col2:
    recommend_clicked = st.button("Recommend")

if recommend_clicked:
    names, posters, star_strs, embed_keys = recommend(selected_movie)

    html = """
    <style>
    .recommendation-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 22px; padding: 20px; justify-items: center; box-sizing: border-box; }
    .movie-card { background: #181818; border-radius: 10px; padding: 10px; width: 200px; text-align: center; box-shadow: 0 6px 18px rgba(0,0,0,0.5); transition: transform 0.18s ease; }
    .movie-card:hover { transform: translateY(-6px); }
    .movie-img { width: 180px; height: 260px; object-fit: cover; border-radius: 6px; display: block; margin: 0 auto; }
    .movie-title { margin-top: 8px; font-size: 15px; font-weight: 600; color: #fff; }
    .stars { color: #ffcc00; font-size: 18px; margin-top: 6px; }
    .watch-btn { display:inline-block; margin-top:8px; background:#e50914; color:#fff; padding:6px 10px; border-radius:6px; text-decoration:none; font-weight:600; cursor:pointer; }
    .card-popup { position: fixed; width: 450px; height: 250px; background: #0f0f0f; border-radius: 8px; box-shadow: 0 20px 60px rgba(0,0,0,0.7); z-index: 9999; display: none; overflow: hidden; padding: 8px; }
    .card-popup iframe { width: 100%; height: calc(100% - 34px); border: none; border-radius: 6px; display:block; }
    .card-popup .popup-header { height: 34px; display:flex; align-items:center; justify-content:space-between; gap:10px; padding:0 8px; }
    .card-popup .popup-title { color:#fff; font-weight:600; font-size:14px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:360px; }
    .card-popup .popup-close { color:#fff; font-size:20px; cursor:pointer; padding:2px 6px; background:transparent; border-radius:4px; }
    .card-popup::after { content: ""; position: absolute; width: 0; height: 0; border-left: 8px solid transparent; border-right: 8px solid transparent; border-bottom: 8px solid rgba(15,15,15,1); top: -8px; left: 20px; }
    @media(max-width:900px){ .recommendation-grid { grid-template-columns: repeat(2,1fr); } .card-popup { width: 420px; height: 230px; } }
    @media(max-width:480px){ .recommendation-grid { grid-template-columns: repeat(1,1fr); } .card-popup { width: 320px; height: 200px; left: 10px !important; top: 60px !important; } }
    </style>

    <div class="recommendation-grid">
    """

    for idx, (nm, p_url, s_str, e_key) in enumerate(zip(names, posters, star_strs, embed_keys)):
        safe_nm = nm.replace("'", "&#39;").replace('"', "&quot;")
        data_attr = f"data-embed='{e_key}'" if e_key else "data-embed=''"
        html += f"""
        <div class="movie-card" data-card-id="{idx}">
            <img src="{p_url}" class="movie-img" />
            <div class="movie-title">{safe_nm}</div>
            <div class="stars">{s_str}</div>
            <a href="#" class="watch-btn" {data_attr} data-cardid="{idx}">{'Watch Trailer' if e_key else 'No Trailer'}</a>
        </div>
        """

    html += "</div>"

    html += """
    <div class="card-popup" id="cardPopup" aria-hidden="true">
      <div class="popup-header">
        <div class="popup-title" id="popupTitle"></div>
        <div class="popup-close" id="popupClose">&times;</div>
      </div>
      <iframe id="popupFrame" src="" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>

    <script>
    (function(){
      const popup = document.getElementById('cardPopup');
      const frame = document.getElementById('popupFrame');
      const closeBtn = document.getElementById('popupClose');
      const popupTitle = document.getElementById('popupTitle');

      function getRect(el){ return el.getBoundingClientRect(); }

      function showPopupForCard(cardEl, titleText, embedKey){
        const rect = getRect(cardEl);
        const popupW = popup.offsetWidth;
        const popupH = popup.offsetHeight;

        let leftPos = rect.left + (rect.width/2) - (popupW/2);
        const topPos = rect.top - popupH - 14;

        const maxLeft = window.innerWidth - popupW - 10;
        if(leftPos < 8) leftPos = 8;
        if(leftPos > maxLeft) leftPos = maxLeft;

        const arrowLeft = Math.max(16, Math.min(popupW - 24, (rect.left + rect.width/2) - leftPos - 8));
        popup.style.setProperty('--arrow-left', arrowLeft + 'px');

        popup.style.left = leftPos + 'px';
        popup.style.top = topPos + 'px';
        popup.style.display = 'block';
        popup.setAttribute('aria-hidden','false');

        popupTitle.textContent = titleText;
        if(embedKey){
          frame.src = 'https://www.youtube.com/embed/' + embedKey + '?autoplay=1&rel=0';
        } else { frame.src = ''; }
      }

      function hidePopup(){
        popup.style.display = 'none';
        popup.setAttribute('aria-hidden','true');
        frame.src = '';
      }

      document.querySelectorAll('.watch-btn').forEach(btn => {
        btn.addEventListener('click', function(e){
          e.preventDefault();
          const embedKey = this.getAttribute('data-embed');
          const cardId = this.getAttribute('data-cardid');
          const cardEl = document.querySelector(`.movie-card[data-card-id="${cardId}"]`);
          const titleText = cardEl ? (cardEl.querySelector('.movie-title')?.textContent || '') : '';
          if(!embedKey) return;
          showPopupForCard(cardEl, titleText, embedKey);
        });
      });

      closeBtn.addEventListener('click', hidePopup);
      document.addEventListener('click', function(ev){
        if(popup.style.display === 'block'){
          const withinPopup = ev.target.closest && ev.target.closest('#cardPopup');
          const isWatchBtn = ev.target.closest && ev.target.closest('.watch-btn');
          if(!withinPopup && !isWatchBtn){ hidePopup(); }
        }
      });
      document.addEventListener('keydown', function(ev){
        if(ev.key === 'Escape' && popup.style.display === 'block'){ hidePopup(); }
      });

      const styleEl = document.createElement('style');
      document.head.appendChild(styleEl);
      styleEl.textContent = `.card-popup::after { left: var(--arrow-left, 20px) !important; }`;
    })();
    </script>
    """

    components.html(html, height=900, scrolling=True)

st.markdown("<div class='footer'>© 2025 Movie Recommendation System | Made with ❤️ by Shreya</div>", unsafe_allow_html=True)
