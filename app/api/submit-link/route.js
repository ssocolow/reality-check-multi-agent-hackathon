import FirecrawlApp from '@mendable/firecrawl-js';

import { NextResponse } from 'next/server';

const app = new FirecrawlApp({apiKey: "fc-1855ceb9a3754a51b10b7c30838c0f14"});

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

  // const crawlResponse = "responseeee !"

  // if (!crawlResponse.success) {
  //   throw new Error(`Failed to crawl: ${crawlResponse.error}`)
  // }

  console.log(crawlResponse);

    // Respond with success
  return NextResponse.json(
    {
      successful: true,
      message: crawlResponse
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