parts = "";
$(".thumbnail").each(function(i, e){
    var p = $(e).parents(".echo-li-left-wrapper")[0];
    var title = $(p).find('.echo-title').text();
    if (!e.src) return;
    var src = e.src.split('/');
    var content = src.slice(0, 7).join('/') +  '/';
    parts += ' ' + content + ' "' + src[4] + ' ' + title.replace(/[\/><|?:]/g, ' ') + '"';
});
console.log('python echodownload.py' + parts);