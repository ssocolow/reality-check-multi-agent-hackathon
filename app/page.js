
// export default function Home() {
//   return (
//   <h1> HI </h1>
//   );
// }
'use client';
import { remark } from 'remark';
import html from 'remark-html';

// import react from ''
export default function Home() {


  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(e);
    document.getElementById('waiting').innerHTML = "Waiting for responses, takes ~15 seconds"
    let link = e.target[0].value;

    console.log(link);

    const response = await fetch('/api/submit-link', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({link: link}),
    });

    let responseJSON = await response.json();
    let responseText = responseJSON.message;

    console.log(responseText);
    const processedContent = await remark().use(html).process(responseText);
    const contentHtml = "<h2>Multi-Agent Response</h2>" + processedContent.toString();
    document.getElementById('response').innerHTML = contentHtml;

    
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-white text-black p-4">
      <h1 className="text-4xl font-bold mb-2">Reality Check</h1>
      <h2 className="text-xl text-purple-700 mb-6">Enter the link of an article or website for three LLMs to consider what might be misinforming or confusing</h2>

      <div className="space-x-2 w-full max-w-2xl border border-gray-300 rounded-xl p-4 bg-gradient-to-r from-red-100 to-blue-100">
        <form onSubmit={handleSubmit} className='relative'>
          <input type='text'
            id="searchy"
            autoComplete='off'
            autoFocus
            spellCheck="false"
            //data-effective-keyword
            data-autoload="false"
            tabIndex="1"
            placeholder="Enter Keywords or Filter By Category Below "
            className="w-full p-2 rounded-md border border-gray-300 mb-2"
          />

        </form>
        </div>
        <h3 style={{color: "blue"}} id='waiting'></h3>
        <div id='response'></div>
      </div>
  );
}