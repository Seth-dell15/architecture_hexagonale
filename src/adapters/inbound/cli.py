from src.use_cases.create_order import CreateOrder
from src.use_cases.get_order import GetOrder
from src.use_cases.list_orders import ListOrders
from src.use_cases.update_order import UpdateOrder
from src.use_cases.delete_order import DeleteOrder

class ShopLiteCLI:
    """Adaptateur primaire (Inbound) gérant l'interface en ligne de commande."""

    def __init__(
        self,
        create_order: CreateOrder,
        get_order: GetOrder,
        list_orders: ListOrders,
        update_order: UpdateOrder,
        delete_order: DeleteOrder
    ):
        self.create_order = create_order
        self.get_order = get_order
        self.list_orders = list_orders
        self.update_order = update_order
        self.delete_order = delete_order

    def run(self):
        """Lance la boucle principale du menu interactif."""
        while True:
            print("\n=== ShopLite — Gestion des commandes ===")
            print("1. Créer une commande")
            print("2. Lister toutes les commandes")
            print("3. Consulter une commande par ID")
            print("4. Mettre à jour une commande")
            print("5. Supprimer une commande")
            print("6. Quitter")

            choice = input("\nChoisissez une option (1-6) : ").strip()

            if choice == "1":
                self._handle_create()
            elif choice == "2":
                self._handle_list()
            elif choice == "3":
                self._handle_get()
            elif choice == "4":
                self._handle_update()
            elif choice == "5":
                self._handle_delete()
            elif choice == "6":
                print("Au revoir !")
                break
            else:
                print("Option invalide, veuillez choisir entre 1 et 6.")

    def _handle_create(self):
        print("\n--- Création d'une commande ---")
        customer_name = input("Nom du client : ").strip()
        if not customer_name:
            print("Erreur : le nom du client est obligatoire.")
            return

        amount_text = input("Montant HT : ").strip()
        try:
            amount_ht = float(amount_text)
        except ValueError:
            print("Erreur : le montant doit être un nombre.")
            return

        if amount_ht <= 0:
            print("Erreur : le montant doit être positif.")
            return

        loyalty_answer = input("Client fidèle ? (oui/non) : ").strip()
        is_loyal = loyalty_answer.lower() == "oui"

        try:
            order = self.create_order.execute(customer_name, amount_ht, is_loyal)
            print("\nCommande créée avec succès !")
            print(f"Numéro : {order.id}")
            print(f"Client : {order.customer_name}")
            print(f"Montant HT : {order.amount_ht:.2f} €")
            print(f"Remise : {order.discount:.2f} €")
            print(f"Montant TTC : {order.amount_ttc:.2f} €")
        except ValueError as e:
            print(f"Erreur : {e}")

    def _handle_list(self):
        print("\n--- Liste des commandes ---")
        orders = self.list_orders.execute()
        if not orders:
            print("Aucune commande enregistrée.")
            return
        for o in orders:
            print(f"ID: {o.id} | Client: {o.customer_name} | HT: {o.amount_ht:.2f}€ | Remise: {o.discount:.2f}€ | TTC: {o.amount_ttc:.2f}€ | Date: {o.created_at}")

    def _handle_get(self):
        print("\n--- Consultation d'une commande ---")
        try:
            order_id = int(input("Entrez l'ID de la commande : ").strip())
            order = self.get_order.execute(order_id)
            if not order:
                print(f"Aucune commande trouvée avec l'ID {order_id}.")
                return
            print(f"\nDétails de la commande #{order.id} :")
            print(f"Client : {order.customer_name}")
            print(f"Montant HT : {order.amount_ht:.2f} €")
            print(f"Remise : {order.discount:.2f} €")
            print(f"Montant TTC : {order.amount_ttc:.2f} €")
            print(f"Date : {order.created_at}")
        except ValueError:
            print("Erreur : L'ID doit être un nombre entier.")

    def _handle_update(self):
        print("\n--- Mise à jour d'une commande ---")
        try:
            order_id = int(input("Entrez l'ID de la commande à modifier : ").strip())
            customer_name = input("Nouveau nom du client : ").strip()
            amount_text = input("Nouveau montant HT : ").strip()
            loyalty_answer = input("Client fidèle ? (oui/non) : ").strip()

            amount_ht = float(amount_text)
            is_loyal = loyalty_answer.lower() == "oui"

            order = self.update_order.execute(order_id, customer_name, amount_ht, is_loyal)
            print(f"\nCommande {order.id} mise à jour avec succès !")
            print(f"Nouveau montant TTC : {order.amount_ttc:.2f} €")
        except ValueError as e:
            print(f"Erreur : {e}")

    def _handle_delete(self):
        print("\n--- Suppression d'une commande ---")
        try:
            order_id = int(input("Entrez l'ID de la commande à supprimer : ").strip())
            self.delete_order.execute(order_id)
            print(f"\nCommande {order_id} supprimée avec succès.")
        except ValueError as e:
            print(f"Erreur : {e}")