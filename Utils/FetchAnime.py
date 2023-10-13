import requests as req


class AnimeScrapper:
    def __init__(self, base_url: str, query: str) -> None:
        self.base_url = base_url
        self.query = query

    def getAnimeByID(self, variables: dict) -> list:
        res = req.post(
            url=self.base_url,
            json={
                'query': self.query,
                'variables': variables
            }
        )

        return [res.json(), res.headers["X-RateLimit-Remaining"]]


if __name__ == '__main__':
    scrapper = AnimeScrapper(
        base_url='https://graphql.anilist.co',
        query='''
            query ($id : Int) {
            Media(id: $id) {
                title {
                    english
                },
                type,
                startDate {
                    year
                    month
                    day
                }
                endDate {
                    year
                    month
                    day
                }
                meanScore,
                genres
            }
        }
    '''
    )

    res = scrapper.getAnimeByID(variables={'id': 1})

    print(res["data"])
