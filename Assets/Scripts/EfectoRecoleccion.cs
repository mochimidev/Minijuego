using TMPro;
using UnityEngine;

public class EfectoRecoleccion : MonoBehaviour
{
    private const float Duracion = 0.8f;

    private SpriteRenderer spriteRenderer;
    private TMP_Text texto;
    private float tiempo;

    public void Configurar(string nombreItem)
    {
        spriteRenderer = GetComponent<SpriteRenderer>();

        GameObject textoObjeto = new GameObject("Texto feedback");
        textoObjeto.transform.SetParent(transform);
        textoObjeto.transform.localPosition = new Vector3(0f, 0.75f, 0f);

        texto = textoObjeto.AddComponent<TextMeshPro>();
        texto.text = "+ " + nombreItem;
        texto.fontSize = 2.2f;
        texto.alignment = TextAlignmentOptions.Center;
        texto.color = new Color(1f, 0.84f, 0.36f, 1f);
        texto.sortingOrder = spriteRenderer != null ? spriteRenderer.sortingOrder + 1 : 3;
    }

    private void Update()
    {
        tiempo += Time.deltaTime;
        float progreso = Mathf.Clamp01(tiempo / Duracion);

        transform.position += Vector3.up * Time.deltaTime * 1.5f;
        transform.Rotate(Vector3.forward, Time.deltaTime * 90f);
        transform.localScale = Vector3.one * Mathf.Lerp(1.15f, 1.65f, progreso);

        float alpha = 1f - progreso;
        if (spriteRenderer != null)
        {
            Color color = spriteRenderer.color;
            color.a = alpha;
            spriteRenderer.color = color;
        }

        if (texto != null)
        {
            Color colorTexto = texto.color;
            colorTexto.a = alpha;
            texto.color = colorTexto;
        }

        if (tiempo >= Duracion)
        {
            Destroy(gameObject);
        }
    }
}
