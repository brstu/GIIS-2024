using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class hero : entity
{
    [SerializeField] private float speed = 3f;
    [SerializeField] private int lives = 3;
    [SerializeField] private float jumpforce = 12f;
    private bool isGrounded = false;

    private Rigidbody2D rb;
    private Animator anim;
    private SpriteRenderer sprite;

    public static hero Instance { get; set; }

    private States State
    {
        get { return (States)anim.GetInteger("state"); }
        set { anim.SetInteger("state", (int)value); }
    }

    private void Awake()
    {
        Instance = this;
        rb = GetComponent<Rigidbody2D>();
        anim = GetComponent<Animator>();
        sprite = GetComponentInChildren<SpriteRenderer>();
    }

    private void FixedUpdate()
    {
        CheckGround();
    }

    private void Update()
    {
        if (isGrounded)  State = States.idle; 

        if (Input.GetButton("Horizontal"))
            Run();
        if (isGrounded && Input.GetButtonDown("Jump"))
            Jump();
        if (transform.position.y < -9f)
            SceneManager.LoadScene(1);
    }

    private void Run()
    {
       if (isGrounded) { State = States.run; }
       Vector3 dir = transform.right * Input.GetAxis("Horizontal");
       transform.position = Vector3.MoveTowards(transform.position, transform.position + dir, speed * Time.deltaTime);
       sprite.flipX = dir.x < 0.0f;  
    
    }

    private void Jump()
    {
        rb.AddForce(transform.up * jumpforce, ForceMode2D.Impulse);
    }

    private void CheckGround()
    {
        Collider2D[] collider = Physics2D.OverlapCircleAll(transform.position, 0.3f);
        isGrounded = collider.Length > 1;

        if (!isGrounded) State = States.jump;
    }

    public override void GetDamage()
    {
        lives -= 1;
        Debug.Log(lives);
        if (lives < 1)
        {
            SceneManager.LoadScene(1);
        }
    }
    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.tag == "Finish")
        {
            SceneManager.LoadScene(2);
        }
    }
}


public enum States
{
    idle,
    jump,
    run
}