import FirecrawlApp from '@mendable/firecrawl-js';

import { NextResponse } from 'next/server';

const app = new FirecrawlApp({apiKey: "fc-44848be39e2e459f8feea4003dd9b168"});

export async function POST(req) {
  const link = await req.json();
  console.log(link);

  if (!link) {
    return res.status(400).json({ error: 'Link is required' });
  }

  console.log('Received link:', link);

  const crawlResponse = await app.crawlUrl(link, {
    limit: 100,
    scrapeOptions: {
        formats: ['markdown', 'html'],
    }
  })

  if (!crawlResponse.success) {
    throw new Error(`Failed to crawl: ${crawlResponse.error}`)
  }

  console.log(crawlResponse);

    // Respond with success
  return NextResponse.json(
    {
      successful: true,
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