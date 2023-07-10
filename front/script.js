const getList = async () => {

    let url = 'http://127.0.0.1:5000/pacientes';
    fetch(url, {
      method: 'get',
    })
      .then((response) => response.json())
      .then((data) => {
        data.pacientes.forEach(item => insertList(item.nome, item.valor, item.diadasemana, item.comentario))
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }

getList()

const postItem = async (inputPaciente, inputValor, inputDia, inputComent) => {
    const formData = new FormData();
    formData.append('nome', inputPaciente);
    formData.append('valor', inputValor);
    formData.append('diadasemana', inputDia);
    formData.append('comentario', inputComent);
  
    let url = 'http://127.0.0.1:5000/paciente';
    fetch(url, {
      method: 'post',
      body: formData
    })
      .then((response) => response.json())
      .catch((error) => {
        console.error('Error:', error);
      });
  }
  

  const insertButton = (parent) => {
    let span = document.createElement("span");
    let txt = document.createTextNode("\u00D7");
    span.className = "close";
    span.appendChild(txt);
    parent.appendChild(span);
  }
  

  const removeElement = () => {
    let close = document.getElementsByClassName("close");
   // var table = document.getElementById('myTable');
    let i;
    for (i = 0; i < close.length; i++) {
      close[i].onclick = function () {
        let div = this.parentElement.parentElement;
        const pacienteItem = div.getElementsByTagName('td')[0].innerHTML
        if (confirm("Você tem certeza?")) {
          div.remove()
          deleteItem(pacienteItem)
          alert("Removido!")
        }
      }
    }
  }
  

  const deleteItem = (item) => {
    console.log(item)
    let url = 'http://127.0.0.1:5000/paciente?nome=' + item;
    fetch(url, {
      method: 'delete'
    })
      .then((response) => response.json())
      .catch((error) => {
        console.error('Error:', error);
      });
  }
  

  const newItem = () => {
    let inputPaciente = document.getElementById("newPaciente").value;
    let inputValor = document.getElementById("newValor").value;
    let inputDia = document.getElementById("newDia").value;
    let inputComent = document.getElementById("newComent").value;
  
    if (inputPaciente === '') {
      alert("Escreva o nome de um paciente!");
    } else if (isNaN(inputValor)) {
      alert("Valor precisa ser em número!");
    } else {
      insertItem(inputPaciente, inputValor, inputDia, inputComent)
      postItem(inputPaciente, inputValor, inputDia, inputComent)
      alert("Paciente adicionado!")
    }
  }
  

  const insertItem = (nome, valor, diadasemana, comentario) => {
    var item = [nome, valor, diadasemana, comentario];
    var table = document.getElementById('myTable');
    var row = table.insertRow();
  
    for (var i = 0; i < item.length; i++) {
      var cel = row.insertCell(i);
      cel.textContent = item[i];
    }
    insertButton(row.insertCell(-1))
    document.getElementById("newPaciente").value = "";
    document.getElementById("newValor").value = "";
    document.getElementById("newDia").value = "";
    document.getElementById("newComent").value = "";
  
    removeElement()
  }