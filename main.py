import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계")

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

# 데이터 불러오기
url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
df = pd.read_csv(url)

# 여러 장르가 있으면 첫 번째 장르만 사용
df["genre_first"] = (
    df["genre"]
    .fillna("장르 미상")
    .astype(str)
    .str.split("|")
    .str[0]
)

# 숫자형으로 변환
df["total_audi"] = pd.to_numeric(df["total_audi"], errors="coerce")
df["first_scrn"] = pd.to_numeric(df["first_scrn"], errors="coerce")
df["first_week_audi"] = pd.to_numeric(
    df["first_week_audi"], errors="coerce"
)


# =============================
# 1. 장르별 영화 편수
# =============================
st.header("1. 장르별 영화 편수")

genre_count = df["genre_first"].value_counts().reset_index()
genre_count.columns = ["장르", "영화 편수"]

fig1 = px.pie(
    genre_count,
    names="장르",
    values="영화 편수",
    hole=0.45,
    title="장르별 영화 편수"
)

fig1.update_traces(
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "편수: %{value}편<br>"
        "비율: %{percent}"
        "<extra></extra>"
    )
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "어떤 장르의 영화가 가장 많이 포함되어 있는지 알 수 있다."
)

st.divider()


# =============================
# 2. 장르별 영화 총 관객 트리맵
# =============================
st.header("2. 장르별 영화 총 관객")

treemap_df = df.dropna(
    subset=["total_audi"]
).copy()

fig2 = px.treemap(
    treemap_df,
    path=["genre_first", "movieNm"],
    values="total_audi",
    title="장르별 영화 총 관객"
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "각 장르에 어떤 영화가 포함되어 있고, 영화별 총 관객 규모가 얼마나 다른지 알 수 있다."
)

st.divider()


# =============================
# 3. 총 관객수 히스토그램
# =============================
st.header("3. 총 관객수 분포")

hist_df = df.dropna(
    subset=["total_audi"]
).copy()

fig3 = px.histogram(
    hist_df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객수 분포",
    labels={
        "total_audi": "총 관객수",
        "count": "영화 편수"
    }
)

fig3.update_traces(
    hovertemplate=(
        "총 관객수: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

st.plotly_chart(fig3, use_container_width=True)

bin_counts = hist_df["total_audi"].groupby(
    pd.cut(
        hist_df["total_audi"],
        bins=20,
        include_lowest=True
    )
).size()

most_common_bin = bin_counts.idxmax()

max_row = hist_df.loc[
    hist_df["total_audi"].idxmax()
]

max_movie = max_row["movieNm"]
max_audience = int(max_row["total_audi"])

st.markdown(
    f"**이 그래프로 알 수 있는 것:** "
    f"대부분의 영화는 **{most_common_bin.left:,.0f}명 ~ "
    f"{most_common_bin.right:,.0f}명** 구간에 몰려 있다. "
    f"가장 관객이 많은 영화는 **{max_movie}**로, "
    f"총 **{max_audience:,}명**의 관객을 기록했다."
)

st.divider()


# =============================
# 4. 개봉일 스크린수와 총 관객의 관계
# =============================
st.header("4. 개봉일 스크린수와 총 관객의 관계")

scatter_df = df.dropna(
    subset=[
        "first_scrn",
        "total_audi",
        "movieNm",
        "genre_first"
    ]
).copy()

fig4 = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre_first",
    hover_name="movieNm",
    title="개봉일 스크린수와 총 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "genre_first": "장르"
    }
)

fig4.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,}개<br>"
        "총 관객수: %{y:,}명"
        "<extra></extra>"
    )
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "개봉일에 확보한 스크린 수와 영화의 총 관객 수가 어떤 관계를 보이는지 비교할 수 있다."
)

st.divider()


# =============================
# 5. 장르별 총 관객수 상자 그림
# =============================
st.header("5. 장르별 총 관객수 분포")

box_df = df.dropna(
    subset=[
        "genre_first",
        "total_audi",
        "movieNm"
    ]
).copy()

genre_counts = box_df["genre_first"].value_counts()

valid_genres = genre_counts[
    genre_counts >= 10
].index

box_df = box_df[
    box_df["genre_first"].isin(valid_genres)
].copy()

fig5 = px.box(
    box_df,
    x="genre_first",
    y="total_audi",
    color="genre_first",
    points="outliers",
    hover_name="movieNm",
    title="영화가 10편 이상인 장르의 총 관객수 분포",
    labels={
        "genre_first": "장르",
        "total_audi": "총 관객수"
    }
)

fig5.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "총 관객수: %{y:,}명"
        "<extra></extra>"
    )
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "영화가 10편 이상인 장르별로 총 관객수의 분포와 "
    "유난히 관객수가 많은 영화를 확인할 수 있다."
)

st.divider()


# =============================
# 6. 첫 주 관객을 크기로 나타낸 버블 그래프
# =============================
st.header("6. 개봉일 스크린수·총 관객·첫 주 관객의 관계")

bubble_df = df.dropna(
    subset=[
        "first_scrn",
        "total_audi",
        "first_week_audi",
        "movieNm",
        "genre_first"
    ]
).copy()

fig6 = px.scatter(
    bubble_df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre_first",
    hover_name="movieNm",
    size_max=50,
    title="개봉일 스크린수와 총 관객의 관계 (첫 주 관객 버블)",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "first_week_audi": "첫 주 관객",
        "genre_first": "장르"
    }
)

fig6.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,}개<br>"
        "총 관객수: %{y:,}명<br>"
        "첫 주 관객: %{marker.size:,}명"
        "<extra></extra>"
    )
)

st.plotly_chart(fig6, use_container_width=True)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "개봉일 스크린수와 총 관객의 관계를 확인하면서 "
    "첫 주 관객이 많은 영화가 어떤 크기로 나타나는지 함께 비교할 수 있다."
)

st.divider()


# =============================
# 7. 제작 국가 → 장르 선버스트
# =============================
st.header("7. 제작 국가별 장르 분포")

sunburst_df = df.dropna(
    subset=["nation", "genre_first"]
).copy()

# 제작 국가와 장르별 영화 편수 계산
sunburst_count = (
    sunburst_df
    .groupby(["nation", "genre_first"])
    .size()
    .reset_index(name="영화 편수")
)

fig7 = px.sunburst(
    sunburst_count,
    path=["nation", "genre_first"],
    values="영화 편수",
    title="제작 국가 → 장르별 영화 편수"
)

fig7.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편"
        "<extra></extra>"
    )
)

st.plotly_chart(fig7, use_container_width=True)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "제작 국가별로 어떤 장르의 영화가 많이 포함되어 있는지 알 수 있다."
)

st.divider()
