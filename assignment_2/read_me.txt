Nome: Raphael Soares Ramos
Matrícula: 140160299

Este projeto foi desenvolvido foi desenvolvido em Linux 18.04 64 bits, utilizando a versão 3.4.2 do OpenCV e Python 3.6.5. 

O programa assume que as imagens utilizadas na questão 1 estão na pasta Images.
A questão 1 está no script question_1.py e a 2 no question_2.py.
Execute question_1.py antes de question_2.py!

question_1.py salvará salvará em disco a imagem final sem ruído em bgr. Além de outras imagens intermediárias.
question_2.py exibirá na tela o template utilizado, o template rotacionado e exibirá a imagem obtida em question_1.py
com retângulos pretos em volta mostrando a localização aproximada dos aviões usando a equação pedida no enunciado.

A convolução é feita através da função convolve. Caso queira testar um filtro como o Laplaciano, apenas chame a função convolve
com os seguintes parâmetros: convolve(img, laplacian, 0), onde:
laplacian = np.array((
    [0, 1, 0],
    [1, -4, 1],
    [0, 1, 0]), dtype="int")



