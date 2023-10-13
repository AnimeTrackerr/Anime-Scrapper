# media query that contains meta data for an anime
AnimeMetaData = '''
    media(id: $id) {
        id,
        title {
            english
            romaji
        },
        format,
        synonyms,
        type,
        episodes,
        meanScoreAni : meanScore,
        genres,
        tags {
            name
        },
        status,
        isAdult,
        description,
        season,
        startDate {
            year
            month
            day
        },
        endDate {
            year
            month
            day
        },
        bannerImage,
        coverImage {
            extraLarge
            large
            medium
            color
        },
        characters (sort : $sortCharBasedOn, perPage : $charLimitPerAnime) {
            edges {
                node {
                    name {
                        full
                    }
                    image {
                        medium,
                    }
                }
                role
                voiceActors(language: JAPANESE) {
                    name {
                        full
                    }
                    image {
                        medium
                    }
                }
            }
        },
        studios {
            edges {
                node {
                    name
                }
            }
        }
    }
        
'''

# pagination details to itrate through pages of results
Pagination = '''
    pageInfo {
        total
        currentPage
        lastPage
        hasNextPage
        perPage
    }
'''

# variables to provide the query with
Variables = {
    'page': 1,
    'perPage': 50,
    'charLimitPerAnime': 8,
    'sortCharBasedOn': 'ROLE'
}
