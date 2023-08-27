import jp from 'jsonpath';
import { GITHUB_API_PROJECT_URL } from '../consts';

export async function getGithubTopics (githubName: String): Promise<Array<String>> {
  console.info('githubApi.ts: githubName: ' + githubName);

  // get from github project api
  const response = await fetch(GITHUB_API_PROJECT_URL + githubName);
  const data = await response.json();
/*
  // based on
  // file:///C:/d/r/astro-github-api-plugin/01-01-vanilla-HTML5-starter-page.json
  const dataMock = {
	"name": "01-01-vanilla-HTML5-starter-page",
	"html_url": "https://github.com/roebi/01-01-vanilla-HTML5-starter-page",
	"description": "vanilla HTML 5 starter page - Have you ever heard of this HTML 5 tags ?",
	"homepage": "https://roebi.github.io/01-01-vanilla-HTML5-starter-page/",
	"topics": [
      "html5",
      "html5-template",
      "roebi",
      "starter"
    ]
  };
  const data = dataMock;
*/
  // https://www.npmjs.com/package/jsonpath MIT License
  return jp.query(data, '$.topics[*]') as Array<String>;
}
