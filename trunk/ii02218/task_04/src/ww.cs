using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ww : entity
{
    private float speed = 2f;
    private Vector3 dir;
    private SpriteRenderer sprite;

    private void Start()
    {
        sprite = GetComponentInChildren<SpriteRenderer>();
        dir = transform.right;
    }

    private void Update()
    {
        Move();
    }

    private void Move()
    {
        Collider2D[] colliders = Physics2D.OverlapCircleAll(transform.position + transform.up * 0.1f + transform.right * dir.x * 0.7f, 0.1f);
        if (colliders.Length > 0) dir *= -1f;
        transform.position = Vector3.MoveTowards(transform.position, transform.position + dir, speed * Time.deltaTime);
        sprite.flipX = dir.x > 0.0f; 
    }

    private void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.gameObject == hero.Instance.gameObject)
        {
            hero.Instance.GetDamage();
        }
    }
}
