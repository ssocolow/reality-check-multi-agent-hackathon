import FirecrawlApp from '@mendable/firecrawl-js';

import { NextResponse } from 'next/server';
// Node.js (JavaScript)
const { exec } = require('child_process');
const fs = require('node:fs');


const app = new FirecrawlApp({apiKey: "fc-1855ceb9a3754a51b10b7c30838c0f14"});

function executeCommand(command) {
  return new Promise((resolve, reject) => {
    exec(command, (error, stdout, stderr) => {
      if (error) {
        reject(`exec error: ${error}`);
        return;
      }
      if (stderr) {
        reject(`stderr: ${stderr}`);
        return;
      }
      resolve(stdout);
    });
  });
}
export async function POST(req) {
  const { link } = await req.json();
  console.log(link);

  console.log('Received link:', link);

  const crawlResponse = await app.crawlUrl(link, {
    limit: 100,
    scrapeOptions: {
        formats: ['markdown', 'html'],
    }
  })
  // console.log(crawlResponse);
  // console.log(crawlResponse.data);
  // console.log(crawlResponse.data[0]);
  // console.log(crawlResponse.data[0].markdown);
  const content = crawlResponse.data[0].markdown;
  // const crawlResponse = "hi my name is joe and i like eating pizza to stay away from covid"
 
  fs.writeFile('output.txt', content, err => {
    if (err) {
      console.error(err);
    } else {
      // file written successfully
      console.log('file written successfully');
    }
  });

 

  let llmSummary = await executeCommand('python3 script.py');
  // if (!crawlResponse.success) {
  //   throw new Error(`Failed to crawl: ${crawlResponse.error}`)
  // }

  // console.log(crawlResponse);

    // Respond with success
  return NextResponse.json(
    {
      successful: true,
      message: llmSummary
    },
    {
      status: 200
    }
  )
}
//     const { link } = req.body;

//     if (!link) {
//       return res.status(400).json({ error: 'Link is required' });
//     }

//     console.log('Received link:', link);

// const crawlResponse = await app.crawlUrl(link, {
//     limit: 100,
//     scrapeOptions: {
//         formats: ['markdown', 'html'],
//     }
//     })

//     if (!crawlResponse.success) {
//     throw new Error(`Failed to crawl: ${crawlResponse.error}`)
//     }

//     console.log(crawlResponse);

//     // Respond with success
//     return res.status(200).json({ message: 'Link received successfully' });
//   } else {
//     // Handle any other HTTP methods
//     return (<Home></Home>);
//     // res.setHeader('Allow', ['POST']);
//     // res.status(405).end(`Method ${req.method} Not Allowed`);


// }