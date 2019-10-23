// EXAMPLE in HTML
// myVarTest = likeFunction( {{ MEME.id | safe }} );
// <script>
// myVarTest = likeFunction( {{ MEME.id | safe }} );
// </script>
function likeFunction(memeId){
    console.log('Passing var - memeId: '+memeId);
return memeId
}