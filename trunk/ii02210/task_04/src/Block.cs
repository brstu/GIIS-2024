using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace tetris_
{
    public abstract class Block
    {
        protected abstract Position[][] Tiles { get; }

        protected abstract Position StartOffset { get; }

        public abstract int Id { get; }

        private int rotationState;
        private Position @readonly;

        protected Block()
        {
            @readonly = new Position(StartOffset.Row, StartOffset.Column);
        }

        public IEnumerable<Position> TilePositions()
        {
            foreach (Position p in Tiles[rotationState]) 
            {
                yield return new Position(p.Row + @readonly.Row, p.Column + @readonly.Column);
            }
        }

        public void RotateCW()
        {
            rotationState = (rotationState + 1) % Tiles.Length;
        }

        public void RotateCCW()
        {
            if (rotationState == 0) rotationState = (rotationState + 4 - 1) % 4;
            else rotationState--;
        }

        public void Move(int rows,  int columns)
        {
            @readonly.Row += rows;
            @readonly.Column += columns;
        }

        public void Reset()
        {
            rotationState = 0;
            @readonly.Row = StartOffset.Row;
            @readonly.Column = StartOffset.Column;
        }
    }
}
