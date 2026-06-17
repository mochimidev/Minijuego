using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FinalNivel : MonoBehaviour
{
    private void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("Player"))
        {
            if (ContadorDiamantes.TodosLosItemsConseguidos)
            {
                GestorEventos.IniciarEventoCompletarNivel();
            }
            else
            {
                Debug.Log("Aun faltan items del disfraz por conseguir.");
            }
        }
    }
}
