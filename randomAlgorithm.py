import random

def random_wavelength_assignment(traffic_matrix, num_wavelengths):
    num_nodes = len(traffic_matrix)
    # Δημιουργούμε μια λίστα με όλες τις αιτήσεις
    requests = []
    
    # Για κάθε ζεύγος κόμβων
    for i in range(num_nodes):
        for j in range(num_nodes):
            # Αν υπάρχει αίτηση (δηλαδή > 0 στον πίνακα)
            if traffic_matrix[i][j] > 0:
                # Προσθέτουμε τόσες αιτήσεις όσες ζητούνται
                for _ in range(traffic_matrix[i][j]):
                    requests.append((i, j))