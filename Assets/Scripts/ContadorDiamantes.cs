using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class ContadorDiamantes : MonoBehaviour
{
    public TMP_Text Diamantes;
    public static int DiamantesConseguidos { get; private set; } = 0;
    public static int TotalDiamantes { get; private set; } = 0;

    public static bool TodosLosItemsConseguidos
    {
        get { return TotalDiamantes > 0 && DiamantesConseguidos >= TotalDiamantes; }
    }

    private void Start() {
        DiamantesConseguidos = 0;
        TotalDiamantes = FindObjectsOfType<Diamante>(true).Length;
        actualizarTexto();
    }

    private void Awake()
    {
        GestorEventos.EventoObtenerDiamante += aumentarDiamantes;
        GestorEventos.EventoMuerteJugador += reiniciarDiamantes;
    }

    private void aumentarDiamantes()
    {
        DiamantesConseguidos += 1;
        actualizarTexto();
    }

    private void reiniciarDiamantes()
    {
        DiamantesConseguidos = 0;
        actualizarTexto();
    }

    private void actualizarTexto()
    {
        if (Diamantes == null)
        {
            return;
        }

        Diamantes.text = TotalDiamantes > 0
            ? DiamantesConseguidos + "/" + TotalDiamantes
            : DiamantesConseguidos.ToString();
    }

    private void OnDestroy()
    {
        GestorEventos.EventoObtenerDiamante -= aumentarDiamantes;
        GestorEventos.EventoMuerteJugador -= reiniciarDiamantes;
    }
}
