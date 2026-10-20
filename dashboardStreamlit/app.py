
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Loja de Carros", page_icon="🚗", layout="wide")

CATALOGO = {
    "Fiat Argo 1.0": {"categoria": "Hatch", "preco": 85000.00},
    "Volkswagen Polo": {"categoria": "Hatch", "preco": 95000.00},
    "Chevrolet Onix": {"categoria": "Hatch", "preco": 90000.00},
    "Toyota Corolla": {"categoria": "Sedan", "preco": 155000.00},
    "Honda Civic": {"categoria": "Sedan", "preco": 180000.00},
    "Jeep Compass": {"categoria": "SUV", "preco": 190000.00},
    "Hyundai Creta": {"categoria": "SUV", "preco": 145000.00},
    "Fiat Toro": {"categoria": "Picape", "preco": 140000.00}
}

if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

st.title("Dashboard")
st.markdown("---")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Seleção de Veículos")

    with st.form("form_carro"):
        carro_nome = st.selectbox("Escolha o Veículo", list(CATALOGO.keys()))
        preco_unit = CATALOGO[carro_nome]["preco"]
        st.caption(f"Preço: R$ {preco_unit:,.2f}")

        quantidade = st.number_input("Quantidade", min_value=1, value=1, step=1)

        btn_adicionar = st.form_submit_button(
            "Botar no Carrinho",
            use_container_width=True
        )

        if btn_adicionar:
            subtotal = preco_unit * quantidade
            st.session_state.carrinho.append({
                "Veículo": carro_nome,
                "Categoria": CATALOGO[carro_nome]["categoria"],
                "Preço (R$)": preco_unit,
                "Quantidade": quantidade,
                "Subtotal (R$)": subtotal
            })
            st.success(f"{carro_nome} adicionado com sucesso!")

    st.subheader("Carrinho")

    if st.session_state.carrinho:
        df_carrinho = pd.DataFrame(st.session_state.carrinho)

        st.dataframe(
            df_carrinho,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Preço (R$)": st.column_config.NumberColumn(
                    "Preço",
                    format="R$ %.2f"
                ),
                "Subtotal (R$)": st.column_config.NumberColumn(
                    "Subtotal",
                    format="R$ %.2f"
                )
            }
        )

        if st.button("Limpar Carrinho", use_container_width=True):
            st.session_state.carrinho = []
            st.rerun()
    else:
        st.info("O carrinho está vazio. Adicione veículos.")

with col2:
    st.subheader("Pagamento")

    total_compra = sum(
        item["Subtotal (R$)"] for item in st.session_state.carrinho
    )

    st.metric("TOTAL DA VENDA", f"R$ {total_compra:,.2f}")

    st.markdown("---")

    valor_recebido = st.number_input(
        "Valor Recebido",
        min_value=0.0,
        value=0.0,
        step=1000.0,
        format="%.2f"
    )

    if total_compra == 0:
        st.warning("Adicione um veículo.")
    else:
        troco = valor_recebido - total_compra

        if valor_recebido == 0:
            st.info("Aguardando o pagamento...")
        elif valor_recebido < total_compra:
            falta = total_compra - valor_recebido
            st.error(
                f"Saldo insuficiente. Faltam R$ {falta:,.2f}."
            )
        else:
            st.success("Venda realizada")
            st.metric("TROCO ", f"R$ {troco:,.2f}")

            with st.expander("Ver Comprovante"):
                st.write(f"Veículos comprados: {len(st.session_state.carrinho)}")
                st.write(f"Total da venda: R$ {total_compra:,.2f}")
                st.write(f"Valor recebido: R$ {valor_recebido:,.2f}")
                st.write(f"Troco: R$ {troco:,.2f}")

            if st.button(
                "Finalizar venda",
                type="primary",
                use_container_width=True
            ):
                st.session_state.carrinho = []
                st.rerun()
