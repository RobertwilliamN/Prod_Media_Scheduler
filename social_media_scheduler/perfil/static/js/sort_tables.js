document.addEventListener('DOMContentLoaded', () => {
    const table = document.querySelector('table');
    const headers = table.querySelectorAll('th');

    headers.forEach((header, index) => {
        header.addEventListener('click', () => {
            if (index >= 6) return; // Não ordenar a coluna 'Ações'
            
            const rows = Array.from(table.querySelectorAll('tbody tr'));
            const isAscending = header.dataset.order === 'asc';
            header.dataset.order = isAscending ? 'desc' : 'asc';

            rows.sort((a, b) => {
                const cellA = a.children[index].textContent.trim();
                const cellB = b.children[index].textContent.trim();

                // Tratar as colunas que devem ser ordenadas como números (ID, Page ID, App ID)
                if (index === 0 || index === 2 || index === 3) {
                    return isAscending
                        ? parseInt(cellA, 10) - parseInt(cellB, 10)
                        : parseInt(cellB, 10) - parseInt(cellA, 10);
                } else { 
                    // Tratar as colunas Nome, Rede Social e País como texto
                    return isAscending
                        ? cellA.localeCompare(cellB)
                        : cellB.localeCompare(cellA);
                }
            });

            const tbody = table.querySelector('tbody');
            rows.forEach(row => tbody.appendChild(row));

            // Atualizar os ícones de ordenação
            headers.forEach(otherHeader => {
                const icon = otherHeader.querySelector('i');
                if (icon) {
                    icon.classList.remove('fa-sort-up', 'fa-sort-down');
                    if (otherHeader === header) {
                        icon.classList.add(isAscending ? 'fa-sort-down' : 'fa-sort-up');
                    } else {
                        icon.classList.add('fa-sort');
                    }
                }
            });
        });
    });
});

