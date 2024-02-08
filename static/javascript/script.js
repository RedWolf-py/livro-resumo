

var btn = document.querySelector('.btn');
const mensagem = document.querySelector('.mensagem');
var span = document.querySelector('span');

btn.addEventListener('click', () => {
    digitar(span);
})


function digitar(span) {
    mensagem.style.display = 'block';
    let texto = span.innerHTML.split('');
    span.innerHTML = '';
    texto.forEach((letra, index) => {
        setTimeout(() => {
            mensagem.innerHTML += letra;
        }, 300 * index)

    });

}
