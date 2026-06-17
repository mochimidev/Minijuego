using UnityEngine;

public class Diamante : MonoBehaviour
{
    [SerializeField] private string nombreItem = "Item del disfraz";
    [SerializeField] private Color colorBrillo = new Color(1f, 0.56f, 1f, 1f);
    [SerializeField] private Sprite[] variantesDisfraz;
    private SpriteRenderer spriteRenderer;

    private readonly string[] nombresDisfraz =
    {
        "Sombrero de brujita",
        "Capa magica",
        "Varita brillante",
        "Botas encantadas",
        "Dulce calabaza",
        "Accesorio final",
        "Maquillaje especial"
    };

    private void Awake()
    {
        spriteRenderer = GetComponent<SpriteRenderer>();
        aplicarVarianteVisual();
        GestorEventos.EventoMuerteJugador += reinvocarDiamante;
    }

    private void aplicarVarianteVisual()
    {
        if (spriteRenderer == null || variantesDisfraz == null || variantesDisfraz.Length == 0)
        {
            return;
        }

        int indice = Mathf.Abs(Mathf.RoundToInt(transform.position.x * 3f + transform.position.y * 5f)) % variantesDisfraz.Length;
        spriteRenderer.sprite = variantesDisfraz[indice];

        if (indice < nombresDisfraz.Length)
        {
            nombreItem = nombresDisfraz[indice];
        }
    }

    private void reinvocarDiamante()
    {
        if (!gameObject.activeInHierarchy)
        {
            gameObject.SetActive(true);
        }
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("Player"))
        {
            crearFeedback();
            GestorEventos.IniciarEventoObtenerDiamante();
            gameObject.SetActive(false);
        }
    }

    private void crearFeedback()
    {
        GameObject feedback = new GameObject("Brillo " + nombreItem);
        feedback.transform.position = transform.position + Vector3.up * 0.2f;
        feedback.transform.localScale = Vector3.one * 1.15f;

        SpriteRenderer feedbackRenderer = feedback.AddComponent<SpriteRenderer>();
        feedbackRenderer.sprite = spriteRenderer != null ? spriteRenderer.sprite : null;
        feedbackRenderer.color = colorBrillo;
        feedbackRenderer.sortingLayerID = spriteRenderer != null ? spriteRenderer.sortingLayerID : 0;
        feedbackRenderer.sortingOrder = spriteRenderer != null ? spriteRenderer.sortingOrder + 2 : 2;

        EfectoRecoleccion efecto = feedback.AddComponent<EfectoRecoleccion>();
        efecto.Configurar(nombreItem);
    }

    private void OnDestroy()
    {
        GestorEventos.EventoMuerteJugador -= reinvocarDiamante;
    }
}
