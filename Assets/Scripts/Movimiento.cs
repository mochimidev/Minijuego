using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Movimiento : MonoBehaviour

{
    private Rigidbody2D rb;
    private BoxCollider2D bc;
    private SpriteRenderer spriteRenderer;
    public int Velocidad;
    public int VelocidadSalto;
    public LayerMask CapaPiso;
    public Sprite SpriteIdle;
    public Sprite SpriteCaminar1;
    public Sprite SpriteCaminar2;
    public Sprite SpriteSalto;
    public Sprite SpriteCaida;
    private float tiempoAnimacion;

    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        bc = GetComponent<BoxCollider2D>();
        spriteRenderer = GetComponent<SpriteRenderer>();
    }

    void Update()
    {
        float movimiento = Input.GetAxis("Horizontal") * Velocidad;
        rb.velocity = new Vector2(movimiento, rb.velocity.y);
        tiempoAnimacion += Time.deltaTime;

        if (spriteRenderer != null && Mathf.Abs(movimiento) > 0.01f)
        {
            spriteRenderer.flipX = movimiento < 0;
        }

        actualizarSprite(movimiento);

        if (enElPiso())
        {
            if (Input.GetButtonDown("Jump"))
            {
                rb.velocity = Vector2.zero;
                rb.AddForce(Vector2.up * VelocidadSalto, ForceMode2D.Impulse);
            }
        }
        else
        {
            float movimientoVertical = Input.GetAxis("Vertical") / 10;
            if (movimientoVertical < 0)
            {
                rb.AddForce(Vector2.up * movimientoVertical, ForceMode2D.Impulse);
            }
        }
    }

    private bool enElPiso()
    {
        return Physics2D.BoxCast(bc.bounds.center, bc.bounds.size, 0, Vector2.down, 0.1f, CapaPiso);
    }

    private void actualizarSprite(float movimiento)
    {
        if (spriteRenderer == null)
        {
            return;
        }

        if (!enElPiso())
        {
            spriteRenderer.sprite = rb.velocity.y >= 0 ? SpriteSalto : SpriteCaida;
            return;
        }

        if (Mathf.Abs(movimiento) > 0.01f)
        {
            spriteRenderer.sprite = Mathf.FloorToInt(tiempoAnimacion * 8f) % 2 == 0 ? SpriteCaminar1 : SpriteCaminar2;
            return;
        }

        spriteRenderer.sprite = SpriteIdle;
    }

    private void OnTriggerStay2D(Collider2D other)
    {
        if (other.gameObject.CompareTag("DobleSalto") && Input.GetButton("Jump"))
        {
            rb.velocity = Vector2.zero;
            rb.AddForce(Vector2.up * VelocidadSalto * 60);
        }
    }
}
