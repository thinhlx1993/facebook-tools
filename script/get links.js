$('.bi6gxh9e > a').map( function() {
    const link = $(this).attr('href');
    if (link && link.includes('videos')) {
        console.log(link);
    }
}).get();