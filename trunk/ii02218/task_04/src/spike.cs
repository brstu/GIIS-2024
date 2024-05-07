using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class spike : MonoBehaviour
{
    private void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.gameObject == hero.Instance.gameObject)
        {
            hero.Instance.GetDamage();
        }
    }
}
