import streamlit as st
import hashlib
import time
import csv
import io
from datetime import datetime

# ----- Définition du bloc -----
class Block:
    def __init__(self, index, votes, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.votes = votes  # liste de dictionnaires
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        content = str(self.index) + str(self.timestamp) + str(self.votes) + self.previous_hash
        return hashlib.sha256(content.encode()).hexdigest()

# ----- Blockchain -----
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_votes = []

    def create_genesis_block(self):
        return Block(0, [{"id": "GENESIS", "candidat": "GENESIS", "heure": datetime.now().isoformat()}], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_vote(self, vote):
        self.pending_votes.append(vote)
        if len(self.pending_votes) == 2:
            self.add_block(self.pending_votes)
            self.pending_votes = []

    def add_block(self, votes):
        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), votes, previous_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash() or current.previous_hash != previous.hash:
                return False
        return True

# ----- Streamlit -----
st.set_page_config(page_title="Vote pour un Candidat", layout="wide")
st.title("🗳️ Système de Vote Électronique via Blockchain")

if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()
if "voted_users" not in st.session_state:
    st.session_state.voted_users = set()

# ----- Liste des candidats -----
candidats = ["Fatima Zahra", "Youssef", "Aya", "Omar", "Nour"]

# ----- Formulaire de vote -----
with st.form("vote_form"):
    user_id = st.text_input("🆔 Identifiant électeur (unique)")
    candidat_choisi = st.selectbox("👤 Votez pour un candidat :", candidats)
    submitted = st.form_submit_button("✅ Soumettre le vote")

    if submitted:
        if not user_id:
            st.warning("⚠️ Veuillez saisir un identifiant.")
        elif user_id in st.session_state.voted_users:
            st.error("❌ Cet identifiant a déjà voté.")
        else:
            vote = {
                "id": user_id,
                "candidat": candidat_choisi,
                "heure": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.blockchain.add_vote(vote)
            st.session_state.voted_users.add(user_id)
            st.success(f"✅ Vote enregistré pour **{candidat_choisi}** à {vote['heure']}")

# ----- Affichage des 3 derniers blocs -----
st.subheader("🧱 Derniers blocs de la Blockchain")
last_blocks = st.session_state.blockchain.chain[-3:]  # Only last 3 blocks

for block in reversed(last_blocks):
    st.markdown(f"""
    <div style="border:2px solid #ccc; padding:15px; border-radius:10px; margin-bottom:20px;">
        <h4>🧱 Bloc #{block.index}</h4>
        <p><strong>🔗 Hash précédent :</strong><br><code>{block.previous_hash}</code></p>
        <p><strong>🗳️ Votes :</strong></p>
        <ul>
            {''.join([f"<li><strong>{v['id']}</strong> a voté pour <strong>{v['candidat']}</strong> à <em>{v['heure']}</em></li>" for v in block.votes])}
        </ul>
        <p><strong>⏱️ Heure du bloc :</strong> {time.ctime(block.timestamp)}</p>
        <p><strong>🔐 Hash du bloc :</strong><br><code>{block.hash}</code></p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander(f"📦 Bloc #{block.index} — {time.ctime(block.timestamp)}"):
        st.markdown(f"**Hash précédent :** `{block.previous_hash}`")
        st.markdown(f"**Hash courant :** `{block.hash}`")
        st.markdown("**Votes dans ce bloc :**")
        for v in block.votes:
            st.markdown(f"- 🆔 {v['id']} a voté pour **{v['candidat']}** à ⏰ {v['heure']}")
        st.markdown("---")

# ----- Vérification de la validité -----
if st.session_state.blockchain.is_chain_valid():
    st.success("✅ Blockchain valide.")
else:
    st.error("❌ Blockchain compromise !")

# ----- Export CSV -----
st.subheader("📤 Exporter la blockchain en CSV")

def export_csv(blockchain):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Bloc", "Date Bloc", "Electeur ID", "Candidat", "Heure du vote", "Hash", "Hash Précédent"])
    for block in blockchain.chain:
        for v in block.votes:
            writer.writerow([
                block.index,
                time.ctime(block.timestamp),
                v['id'],
                v['candidat'],
                v['heure'],
                block.hash,
                block.previous_hash
            ])
    return output.getvalue()

csv_data = export_csv(st.session_state.blockchain)

st.download_button(
    label="📥 Télécharger la blockchain (CSV)",
    data=csv_data,
    file_name="blockchain_votes.csv",
    mime="text/csv"
)


# ----- Fin de l'application -----
# Note: This code is a simple demonstration and should not be used for real voting systems. 