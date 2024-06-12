import numpy as np
import quaternion


def quaternion_inverse(q):
    """
    Calcula el inverso de un quaternion.

    Args:
        q (np.quaternion): El quaternion a invertir.

    Returns:
        np.quaternion: El inverso del quaternion dado.
    """
    return np.quaternion.inverse(q)

def calibrate_sensor_reading(base_quaternion, sensor_reading):
    """
    Aplica una calibración a la lectura de un sensor usando un quaternion base.

    Args:
        base_quaternion (np.quaternion): El quaternion base que define la nueva "frente" del sensor.
        sensor_reading (np.quaternion): La lectura del sensor en quaternion.

    Returns:
        np.quaternion: La lectura del sensor calibrada.
    """
    
    
    
    return calibrated_reading
def quaternion_to_euler_rads(q):
    """
    Convierte un quaternion a ángulos de Euler (en radianes).

    Args:
        q (np.quaternion): El quaternion a convertir.

    Returns:
        tuple: Los ángulos de Euler (roll, pitch, yaw).
    """
    # Extraer componentes del quaternion
    w, x, y, z = q.w, q.x, q.y, q.z

    # Calcular ángulos de Euler
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = np.arctan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = np.clip(t2, -1.0, +1.0)
    pitch_y = np.arcsin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = np.arctan2(t3, t4)

    return roll_x, pitch_y, yaw_z


if __name__ == "__main__":
    # Ejemplo de uso
    # Definir el quaternion base y una lectura del sensor
    base_quaternion = np.quaternion(0.5, 0.5, 0.5, 0.5) # 90º - En el eje Y  - 90, 90, 0
    #base_quaternion = np.quaternion(0.5, 0.5, -0.5, 0.5) # 90º - En el eje Z  - 90, 0, 90
    sensor_reading = np.quaternion( 0.653,  0.653, 0.271, 0.271) # 45º entre XY  - 90, 45, 0

    base_quaternion = base_quaternion.normalized()
    sensor_reading = sensor_reading.normalized()

    base_inverse = quaternion_inverse(base_quaternion)
    calibrated_reading = base_inverse * sensor_reading
    print("Quaternion base:", base_quaternion)
    print("Inversa calculada:", base_inverse)
    print("Lectura del sensor:", sensor_reading)
    print("Lectura calibrada del sensor:", calibrated_reading)

    print()
    calibrated_reading_2 = base_inverse * sensor_reading * base_quaternion
    print("Lectura calibrada del sensor V2:", calibrated_reading_2)

    print()
    calibrated_reading_3 = base_quaternion * sensor_reading * base_inverse
    print("Lectura calibrada del sensor V3:", calibrated_reading_3)
    
    print()
    calibrated_reading_4 =  sensor_reading * base_inverse
    print("Lectura calibrada del sensor V4:", calibrated_reading_4)
    
    print()
    
    # print("EULER - Valor base:", quaternion_to_euler(base_quaternion))
    # print("EULER - Inversa calculada:", quaternion_to_euler(base_inverse))
    # print("EULER - Lectura del sensor:", quaternion_to_euler(sensor_reading))
    # print("EULER - Lectura calibrada del sensor:", quaternion_to_euler(calibrated_reading))
    # print("EULER - Lectura calibrada del sensor 2:", quaternion_to_euler(calibrated_reading_2))
    
    print("Base por inversa", base_quaternion*base_inverse)
    print("lista", base_quaternion.x)
    