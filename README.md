# Discovery helper (versão persistente) para Rinkhals

> **English summary.** Rinkhals app that keeps an Anycubic Kobra 3 V2 in the SSDP multicast group so Anycubic Slicer Next can discover it in LAN mode, even on networks with IGMP snooping. Based on the "Discovery helper" app from Rinkhals.Apps (MIT, Julien Batonnet). Beta: in development and not yet proven.

**Aviso:** projeto beta, em desenvolvimento e ainda não comprovado. Use por sua conta e risco.

Desenvolvido por Raul Ponce Quaresma com assistência de ferramentas de IA.

## O problema

O Anycubic Slicer Next acha a impressora em modo LAN mandando uma mensagem SSDP por multicast (`239.255.255.250`). O firmware original nunca avisa a rede de que está nesse grupo. Por isso, roteadores e switches com *IGMP snooping* não entregam a mensagem, e a impressora não aparece, mesmo estando acessível na rede.

O app original do [Rinkhals.Apps](https://github.com/rinkhals-community/Rinkhals.Apps) manda um único aviso IGMP ao iniciar. A rede esquece o aviso depois de alguns minutos, então quem demorava para conectar não achava mais a impressora.

## O que esta versão muda

- **Fica no grupo:** mantém um socket inscrito no grupo SSDP, e assim o kernel responde às consultas IGMP do roteador. Também repete o aviso IGMPv2 a cada 60 s, para redes sem consultor IGMP.
- **Tolera rede fora do ar:** se a rede ainda não subiu, tenta de novo na volta seguinte.
- **`app.sh`:**
  - roda a partir da pasta do app, porque o `ps` do busybox corta comandos longos e o `get_by_name` não achava o processo;
  - usa `nohup`, para o processo não morrer quando o menu da tela ou o terminal fecha.

## Instalação

1. Copie esta pasta para `/useremain/home/rinkhals/apps/discovery-helper` na impressora (Rinkhals).
2. Ative o app no menu de apps do Rinkhals.
3. Atualizar o app pela loja do Rinkhals substitui esta versão pela original.

## Estado

| Item | Estado |
|---|---|
| O Slicer Next achou a impressora em modo LAN (14/10/2026) | Funcionou |
| Continua funcionando depois de reiniciar a impressora | Não testado |

## Créditos e licença

- Baseado no app "Discovery helper" do [Rinkhals.Apps](https://github.com/rinkhals-community/Rinkhals.Apps), licença MIT, © 2025 Julien Batonnet.
- Modificações: MIT, © 2026 Raul Ponce Quaresma. Veja [LICENSE](LICENSE).

Projeto independente, sem ligação com a Anycubic.
