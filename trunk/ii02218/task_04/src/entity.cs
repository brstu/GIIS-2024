using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class entity : MonoBehaviour
{
  public virtual void GetDamage()
    {

    }
    
    public virtual void Die()
    {
        Destroy(this.gameObject);
    }
}
