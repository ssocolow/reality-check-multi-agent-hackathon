
// export default function Home() {
//   return (
//   <h1> HI </h1>
//   );
// }
'use client';

// import react from ''
export default function Home() {


  const handleSubmit = async (e) => {
    e.preventDefault();
    let link = e.target.value;

    const response = await fetch('/api/submit-link', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({'link': link}),
    });

    console.log(link);
    
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-white text-black p-4">
      <h1 className="text-4xl font-bold mb-2">Reality Check</h1>
      <h2 className="text-xl text-purple-700 mb-6">Enter a link to llms about</h2>

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
      </div>
  );
}