using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraController : MonoBehaviour
{
    [SerializeField] private Transform player;

    private void Update()
    {
        Vector3 pos = player.position;
        pos.z = -10f;
        pos.y += 1f;

        transform.position = Vector3.Lerp(transform.position, pos, Time.deltaTime);
    }
}